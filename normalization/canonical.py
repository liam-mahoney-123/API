"""Canonical model for region-agnostic post-trade equities events."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


CANONICAL_CONTRACT_VERSION = "1.0.0"


REQUIRED_CANONICAL_FIELDS = (
    "event_id",
    "region",
    "source_system",
    "source_message_id",
    "lifecycle_event",
    "trade_id",
    "event_timestamp",
    "side",
    "quantity",
    "price",
    "currency",
    "venue",
    "account",
    "book",
    "sequence_number",
)


@dataclass
class LineageEntry:
    source_path: str
    raw_value: Any
    transforms: list[str] = field(default_factory=list)


@dataclass
class CanonicalEvent:
    event_id: str
    region: str
    source_system: str
    source_message_id: str
    lifecycle_event: str
    trade_id: str
    allocation_id: str | None
    instrument_id: str | None
    instrument_id_type: str | None
    side: str
    quantity: float
    price: float
    notional_local: float | None
    currency: str
    fx_rate_to_usd: float | None
    notional_usd: float | None
    venue: str
    account: str
    book: str
    trade_date: str | None
    settlement_date: str | None
    event_timestamp: str
    sequence_number: int
    ingestion_timestamp: str
    quality_flags: list[str] = field(default_factory=list)
    lineage: dict[str, LineageEntry] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_contract(self) -> dict[str, Any]:
        return {
            "contract_version": CANONICAL_CONTRACT_VERSION,
            "event": {
                "event_id": self.event_id,
                "region": self.region,
                "source_system": self.source_system,
                "source_message_id": self.source_message_id,
                "lifecycle_event": self.lifecycle_event,
                "trade_id": self.trade_id,
                "allocation_id": self.allocation_id,
                "instrument_id": self.instrument_id,
                "instrument_id_type": self.instrument_id_type,
                "side": self.side,
                "quantity": self.quantity,
                "price": self.price,
                "notional_local": self.notional_local,
                "currency": self.currency,
                "fx_rate_to_usd": self.fx_rate_to_usd,
                "notional_usd": self.notional_usd,
                "venue": self.venue,
                "account": self.account,
                "book": self.book,
                "trade_date": self.trade_date,
                "settlement_date": self.settlement_date,
                "event_timestamp": self.event_timestamp,
                "sequence_number": self.sequence_number,
                "ingestion_timestamp": self.ingestion_timestamp,
                "quality_flags": self.quality_flags,
            },
            "lineage": {
                field_name: {
                    "source_path": lineage.source_path,
                    "raw_value": lineage.raw_value,
                    "transforms": lineage.transforms,
                }
                for field_name, lineage in self.lineage.items()
            },
            "metadata": self.metadata,
        }
