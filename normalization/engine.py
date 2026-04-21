"""Normalization engine with validation, dedupe, sequencing, and replay."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from .canonical import CanonicalEvent, LineageEntry, REQUIRED_CANONICAL_FIELDS
from .mappings import ACCOUNT_MAP, BOOK_MAP, REGIONAL_RULES, canonical_region, get_path
from .normalizers import json_hash, normalize_identifier, utc_now_iso


@dataclass
class ProcessingResult:
    published: list[dict[str, Any]] = field(default_factory=list)
    quarantined: list[dict[str, Any]] = field(default_factory=list)
    dropped: list[dict[str, Any]] = field(default_factory=list)
    buffered: list[dict[str, Any]] = field(default_factory=list)
    replayed: list[dict[str, Any]] = field(default_factory=list)


class NormalizationEngine:
    """Stateful cross-region normalization prototype."""

    def __init__(self) -> None:
        self.seen_message_ids: set[str] = set()
        self.latest_sequence: dict[str, int] = {}
        self.out_of_order_buffer: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
        self.quarantine_store: dict[str, dict[str, Any]] = {}
        self.published_store: list[dict[str, Any]] = []
        self.event_history: list[dict[str, Any]] = []
        self.deduped_messages: list[str] = []

    def process_stream(self, raw_events: list[dict[str, Any]]) -> ProcessingResult:
        result = ProcessingResult()
        for raw_event in raw_events:
            outcome = self.process_event(raw_event)
            for bucket_name, item in outcome.items():
                getattr(result, bucket_name).append(item)
        return result

    def process(self, raw_event: dict[str, Any]) -> dict[str, dict[str, Any]]:
        return self.process_event(raw_event)

    def process_event(self, raw_event: dict[str, Any]) -> dict[str, dict[str, Any]]:
        input_region = str(raw_event.get("region", "")).upper()
        region = canonical_region(input_region)
        payload = raw_event.get("payload", {})
        metadata = raw_event.get("metadata", {})
        if region is None:
            quarantine_suffix = normalize_identifier(
                payload.get("id_local") or payload.get("id") or payload.get("eventId") or "UNKNOWN"
            )
            quarantined = self._quarantine(
                raw_event=raw_event,
                reason="UNSUPPORTED_REGION",
                errors=[f"unsupported region '{input_region}'"],
                quarantine_key=f"{input_region}:{quarantine_suffix}",
            )
            return {"quarantined": quarantined}

        rules = REGIONAL_RULES[region]
        source_message_id_raw = get_path(payload, rules["source_message_id"].source_path)
        message_id = normalize_identifier(source_message_id_raw)
        if not message_id:
            quarantined = self._quarantine(
                raw_event=raw_event,
                reason="MISSING_MESSAGE_ID",
                errors=["missing required source message id"],
                quarantine_key=f"{input_region}:UNKNOWN",
            )
            return {"quarantined": quarantined}

        dedupe_key = f"{region}:{message_id}"
        if dedupe_key in self.seen_message_ids:
            dropped = {
                "state": "dropped_duplicate",
                "message_id": dedupe_key,
                "raw_hash": json_hash(raw_event),
                "ingested_at": utc_now_iso(),
                "reason": "duplicate_message_id",
            }
            self.event_history.append(dropped)
            self.deduped_messages.append(dedupe_key)
            return {"dropped": dropped}

        required_errors = self._validate_required_fields(payload, region)
        canonical, mapping_errors = self._map_to_canonical(
            region=region,
            payload=payload,
            metadata=metadata,
            source_message_id=message_id,
        )
        quality_errors = self._quality_checks(canonical)
        errors = required_errors + mapping_errors + quality_errors
        if errors:
            quarantined = self._quarantine(
                raw_event,
                reason="VALIDATION_FAILED",
                errors=errors,
                quarantine_key=f"{input_region}:{message_id}",
            )
            return {"quarantined": quarantined}

        trade_id = canonical.trade_id
        sequence = canonical.sequence_number
        expected_next = self.latest_sequence.get(trade_id, 0) + 1
        if sequence > expected_next:
            buffered = {
                "state": "buffered_out_of_order",
                "trade_id": trade_id,
                "message_id": message_id,
                "sequence": sequence,
                "expected_next": expected_next,
                "ingested_at": utc_now_iso(),
            }
            self.out_of_order_buffer[trade_id][sequence] = raw_event
            self.event_history.append(buffered)
            return {"buffered": buffered}

        if sequence <= self.latest_sequence.get(trade_id, 0):
            dropped = {
                "state": "dropped_sequence_conflict",
                "trade_id": trade_id,
                "message_id": message_id,
                "sequence": sequence,
                "latest_sequence": self.latest_sequence.get(trade_id, 0),
                "ingested_at": utc_now_iso(),
            }
            self.event_history.append(dropped)
            return {"dropped": dropped}

        published_payload = self._publish(canonical)
        self._mark_processed(dedupe_key, trade_id, sequence)
        follow_on = self._drain_buffered_events(trade_id)
        if follow_on:
            published_payload["auto_released_buffered"] = follow_on
        return {"published": published_payload}

    def _validate_required_fields(self, payload: dict[str, Any], region: str) -> list[str]:
        errors: list[str] = []
        for canonical_name, rule in REGIONAL_RULES[region].items():
            if not rule.required:
                continue
            value = get_path(payload, rule.source_path)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"missing required field: payload.{rule.source_path} for canonical.{canonical_name}")
        return errors

    def _quality_checks(self, canonical: CanonicalEvent) -> list[str]:
        errors: list[str] = []
        qty = canonical.quantity
        price = canonical.price
        if qty is None or qty <= 0:
            errors.append("quantity must be positive")
        if price is None or price <= 0:
            errors.append("price must be positive")
        if canonical.event_timestamp is None:
            errors.append("event_timestamp cannot be parsed")
        if canonical.currency is None:
            errors.append("currency is required")
        if canonical.lifecycle_event is None:
            errors.append("lifecycle_event mapping failed")
        for required_field in REQUIRED_CANONICAL_FIELDS:
            value = getattr(canonical, required_field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"missing canonical required field: {required_field}")
        return errors

    def _map_to_canonical(
        self,
        region: str,
        payload: dict[str, Any],
        metadata: dict[str, Any],
        source_message_id: str,
    ) -> tuple[CanonicalEvent, list[str]]:
        rules = REGIONAL_RULES[region]
        values: dict[str, Any] = {}
        lineage: dict[str, LineageEntry] = {}
        errors: list[str] = []

        for canonical_field, rule in rules.items():
            raw_value = get_path(payload, rule.source_path)
            transformed = rule.transform(raw_value)
            values[canonical_field] = transformed
            lineage[canonical_field] = LineageEntry(
                source_path=f"payload.{rule.source_path}",
                raw_value=raw_value,
                transforms=[rule.transform_name],
            )
            if rule.required and transformed is None:
                errors.append(
                    f"canonical.{canonical_field} could not be derived from payload.{rule.source_path}"
                )

        mapped_account = ACCOUNT_MAP.get(region, {}).get(
            values["account"], normalize_identifier(values["account"], "ACC-")
        )
        mapped_book = BOOK_MAP.get(region, {}).get(values["book"], normalize_identifier(values["book"], "BOOK-"))

        notional_local = round(values["quantity"] * values["price"], 6) if values["quantity"] and values["price"] else None
        notional_usd = None
        if notional_local is not None:
            if values.get("fx_rate_to_usd") is not None:
                notional_usd = round(notional_local * values["fx_rate_to_usd"], 6)
            elif values.get("currency") == "USD":
                notional_usd = notional_local

        quality_flags: list[str] = []
        if metadata.get("arrived_late"):
            quality_flags.append("LATE_ARRIVAL")
        if values.get("fx_rate_to_usd") is None and values.get("currency") != "USD":
            quality_flags.append("FX_RATE_MISSING")

        event = CanonicalEvent(
            event_id=f"CANON-{region}-{source_message_id}",
            region=region,
            source_system=str(metadata.get("source_system", "unknown")),
            source_message_id=source_message_id,
            lifecycle_event=values["lifecycle_event"],
            trade_id=values["trade_id"],
            allocation_id=values.get("allocation_id"),
            instrument_id=values.get("instrument_id"),
            instrument_id_type=values.get("instrument_id_type"),
            side=values["side"],
            quantity=values["quantity"],
            price=values["price"],
            notional_local=notional_local,
            currency=values["currency"],
            fx_rate_to_usd=values.get("fx_rate_to_usd"),
            notional_usd=notional_usd,
            venue=values["venue"],
            account=mapped_account,
            book=mapped_book,
            trade_date=values.get("trade_date"),
            settlement_date=values.get("settlement_date"),
            event_timestamp=values["event_timestamp"],
            sequence_number=values["sequence_number"],
            ingestion_timestamp=utc_now_iso(),
            quality_flags=quality_flags,
            lineage=lineage,
            metadata={
                "source_region_input": metadata.get("source_region_input", region),
                "ingest_channel": metadata.get("ingest_channel"),
                "raw_hash": json_hash(payload),
            },
        )
        return event, errors

    def _publish(self, canonical_payload: CanonicalEvent) -> dict[str, Any]:
        envelope = {
            "contract_version": canonical_payload.as_contract()["contract_version"],
            "event_category": "post_trade_equities.normalized",
            "published_at_utc": utc_now_iso(),
            "payload": canonical_payload.as_contract()["event"],
            "lineage": canonical_payload.as_contract()["lineage"],
            "metadata": canonical_payload.as_contract()["metadata"],
        }
        self.published_store.append(envelope)
        self.event_history.append(envelope)
        return envelope

    def _mark_processed(self, message_id: str, trade_id: str, sequence: int) -> None:
        self.seen_message_ids.add(message_id)
        self.latest_sequence[trade_id] = sequence

    def _drain_buffered_events(self, trade_id: str) -> list[dict[str, Any]]:
        released: list[dict[str, Any]] = []
        buffered_for_trade = self.out_of_order_buffer.get(trade_id, {})
        while True:
            expected_next = self.latest_sequence.get(trade_id, 0) + 1
            if expected_next not in buffered_for_trade:
                break
            raw_event = buffered_for_trade.pop(expected_next)
            outcome = self.process_event(raw_event)
            if "published" in outcome:
                released.append(outcome["published"])
            else:
                released.append(outcome)
        if not buffered_for_trade and trade_id in self.out_of_order_buffer:
            del self.out_of_order_buffer[trade_id]
        return released

    def _quarantine(
        self, raw_event: dict[str, Any], reason: str, errors: list[str], quarantine_key: str
    ) -> dict[str, Any]:
        quarantine_id = quarantine_key
        record = {
            "quarantine_id": quarantine_id,
            "state": "quarantined",
            "reason": reason,
            "errors": errors,
            "raw_event": raw_event,
            "raw_hash": json_hash(raw_event),
            "quarantined_at_utc": utc_now_iso(),
        }
        self.quarantine_store[quarantine_id] = record
        self.event_history.append(record)
        return record

    def replay_quarantine(self, fixups: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        replay_results: list[dict[str, Any]] = []
        published: list[dict[str, Any]] = []
        quarantined_outcomes: list[dict[str, Any]] = []
        dropped: list[dict[str, Any]] = []
        buffered: list[dict[str, Any]] = []
        for fix in fixups:
            qid = fix["quarantine_id"]
            quarantined_record = self.quarantine_store.get(qid)
            if quarantined_record is None:
                replay_results.append(
                    {"state": "replay_skipped", "quarantine_id": qid, "reason": "unknown_quarantine_id"}
                )
                continue
            repaired = dict(quarantined_record["raw_event"])
            payload = dict(repaired.get("payload", {}))
            payload.update(fix.get("payload_patch", {}))
            region_override = payload.pop("region_override", None)
            repaired["payload"] = payload
            if region_override:
                repaired["region"] = region_override
            replay_metadata = dict(repaired.get("metadata", {}))
            replay_metadata.update({"replayed": True, **fix.get("replay_metadata", {})})
            repaired["metadata"] = replay_metadata

            outcome = self.process_event(repaired)
            replay_entry = {
                "quarantine_id": qid,
                "repaired_with": fix.get("payload_patch", {}),
                "result": outcome,
            }
            replay_results.append(replay_entry)
            if "published" in outcome:
                published.append(outcome["published"])
            if "quarantined" in outcome:
                quarantined_outcomes.append(outcome["quarantined"])
            if "dropped" in outcome:
                dropped.append(outcome["dropped"])
            if "buffered" in outcome:
                buffered.append(outcome["buffered"])
            if "published" in outcome:
                del self.quarantine_store[qid]
        return {
            "replayed": replay_results,
            "published": published,
            "quarantined": quarantined_outcomes,
            "dropped": dropped,
            "buffered": buffered,
        }

    def replay_quarantined(self, fixes_by_quarantine_id: dict[str, dict[str, Any]]) -> ProcessingResult:
        result = ProcessingResult()
        for quarantine_id, overrides in fixes_by_quarantine_id.items():
            quarantined = self.quarantine_store.get(quarantine_id)
            if quarantined is None:
                result.replayed.append(
                    {
                        "state": "replay_skipped",
                        "quarantine_id": quarantine_id,
                        "reason": "unknown_quarantine_id",
                    }
                )
                continue
            repaired = dict(quarantined["raw_event"])
            repaired.update(overrides)
            outcome = self.process_event(repaired)
            replay_entry = {
                "quarantine_id": quarantine_id,
                "repaired_with": overrides,
                "result": outcome,
            }
            result.replayed.append(replay_entry)
            if "published" in outcome:
                del self.quarantine_store[quarantine_id]
            for bucket_name, item in outcome.items():
                getattr(result, bucket_name).append(item)
        return result

    def quarantine_snapshot(self) -> list[dict[str, Any]]:
        return list(self.quarantine_store.values())

    def published_events(self) -> list[dict[str, Any]]:
        return list(self.published_store)

    def summary(self) -> dict[str, Any]:
        return {
            "published_count": len(self.published_store),
            "quarantine_count": len(self.quarantine_store),
            "deduped_messages": list(self.deduped_messages),
            "buffered_count": sum(len(v) for v in self.out_of_order_buffer.values()),
        }
