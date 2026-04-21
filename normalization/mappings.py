"""Regional schema definitions and code-set mappings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .normalizers import (
    normalize_currency,
    normalize_date,
    normalize_decimal,
    normalize_identifier,
    normalize_timestamp,
)


@dataclass(frozen=True)
class MappingRule:
    source_path: str
    transform: Callable[[Any], Any]
    required: bool = False
    transform_name: str = "identity"


REGION_ALIASES = {
    "US": "US",
    "NA": "US",
    "EU": "EU",
    "EMEA": "EU",
    "APAC": "APAC",
    "AP": "APAC",
}


def canonical_region(region: str) -> str | None:
    return REGION_ALIASES.get(normalize_identifier(region) or "")


def get_path(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def map_code(mapping: dict[str, str], value: Any) -> str | None:
    norm = normalize_identifier(value)
    if norm is None:
        return None
    return mapping.get(norm, norm)


LIFECYCLE_MAP = {
    "US": {"EXEC": "TRADE", "ALLOC": "ALLOCATION", "CORR": "CORRECTION", "CANC": "CANCEL"},
    "EU": {"NEW": "TRADE", "AMEND": "CORRECTION", "CXL": "CANCEL", "ALLOC": "ALLOCATION"},
    "APAC": {"FILL": "TRADE", "BOOK": "ALLOCATION", "AMENDMENT": "CORRECTION", "DELETE": "CANCEL"},
}

SIDE_MAP = {
    "US": {"B": "BUY", "S": "SELL"},
    "EU": {"BUY": "BUY", "SELL": "SELL"},
    "APAC": {"1": "BUY", "2": "SELL"},
}

VENUE_MAP = {
    "XNYS": "NYSE",
    "XNAS": "NASDAQ",
    "XLON": "LSE",
    "LSE": "LSE",
    "SEHK": "HKEX",
    "HKEX": "HKEX",
    "BVMF": "B3",
}

ACCOUNT_MAP = {
    "US": {"AC-001": "ACC-US-ALPHA"},
    "EU": {"UK-PRIME-01": "ACC-EU-PRIME-01", "UK-PRIME-02": "ACC-EU-PRIME-02"},
    "APAC": {"HK_ALPHA_12": "ACC-AP-HK-ALPHA12"},
}

BOOK_MAP = {
    "US": {"EQT_US_LONGLONG": "BOOK-US-LONG"},
    "EU": {"UK_EQ_CORE": "BOOK-EU-CORE"},
    "APAC": {"ASIA_GROWTH": "BOOK-APAC-GROWTH"},
}


def _lifecycle(region: str, value: Any) -> str | None:
    return map_code(LIFECYCLE_MAP[region], value)


def _side(region: str, value: Any) -> str | None:
    return map_code(SIDE_MAP[region], value)


def _venue(value: Any) -> str | None:
    return map_code(VENUE_MAP, value)


REGIONAL_RULES: dict[str, dict[str, MappingRule]] = {
    "US": {
        "source_message_id": MappingRule("eventId", normalize_identifier, True, "normalize_identifier"),
        "lifecycle_event": MappingRule("msgType", lambda v: _lifecycle("US", v), True, "lifecycle_map"),
        "trade_id": MappingRule("tradeRef", lambda v: normalize_identifier(v, "TRD-"), True, "trade_id_prefix"),
        "allocation_id": MappingRule("allocRef", lambda v: normalize_identifier(v, "ALOC-"), False, "allocation_id_prefix"),
        "instrument_id": MappingRule("symbol", normalize_identifier, True, "normalize_identifier"),
        "instrument_id_type": MappingRule("symbol", lambda _: "TICKER", True, "constant:TICKER"),
        "side": MappingRule("side", lambda v: _side("US", v), True, "side_map"),
        "quantity": MappingRule("qty", normalize_decimal, True, "normalize_decimal"),
        "price": MappingRule("px", normalize_decimal, True, "normalize_decimal"),
        "currency": MappingRule("ccy", normalize_currency, True, "normalize_currency"),
        "fx_rate_to_usd": MappingRule("fxRate", normalize_decimal, False, "normalize_decimal"),
        "venue": MappingRule("mic", _venue, True, "venue_map"),
        "account": MappingRule("accountId", normalize_identifier, True, "normalize_identifier"),
        "book": MappingRule("book", normalize_identifier, True, "normalize_identifier"),
        "trade_date": MappingRule("tradeDate", normalize_date, True, "normalize_date"),
        "settlement_date": MappingRule("settlementDate", normalize_date, False, "normalize_date"),
        "event_timestamp": MappingRule("eventTimeMs", normalize_timestamp, True, "normalize_timestamp"),
        "sequence_number": MappingRule("seqNum", lambda v: int(v) if v is not None else None, True, "int"),
    },
    "EU": {
        "source_message_id": MappingRule("id", normalize_identifier, True, "normalize_identifier"),
        "lifecycle_event": MappingRule("lifecycle", lambda v: _lifecycle("EU", v), True, "lifecycle_map"),
        "trade_id": MappingRule("trade_ref", lambda v: normalize_identifier(v, "TRD-"), True, "trade_id_prefix"),
        "allocation_id": MappingRule("allocation_ref", lambda v: normalize_identifier(v, "ALOC-"), False, "allocation_id_prefix"),
        "instrument_id": MappingRule("isin", normalize_identifier, True, "normalize_identifier"),
        "instrument_id_type": MappingRule("isin", lambda _: "ISIN", True, "constant:ISIN"),
        "side": MappingRule("side_code", lambda v: _side("EU", v), True, "side_map"),
        "quantity": MappingRule("shares", normalize_decimal, True, "normalize_decimal"),
        "price": MappingRule("price", normalize_decimal, True, "normalize_decimal"),
        "currency": MappingRule("currency", normalize_currency, True, "normalize_currency"),
        "fx_rate_to_usd": MappingRule("usd_fx", normalize_decimal, False, "normalize_decimal"),
        "venue": MappingRule("venue", _venue, True, "venue_map"),
        "account": MappingRule("acct_num", normalize_identifier, True, "normalize_identifier"),
        "book": MappingRule("book_code", normalize_identifier, True, "normalize_identifier"),
        "trade_date": MappingRule("biz_date", normalize_date, True, "normalize_date"),
        "settlement_date": MappingRule("settle_date", normalize_date, False, "normalize_date"),
        "event_timestamp": MappingRule("timestamp", normalize_timestamp, True, "normalize_timestamp"),
        "sequence_number": MappingRule("sequence", lambda v: int(v) if v is not None else None, True, "int"),
    },
    "APAC": {
        "source_message_id": MappingRule("msg_id", normalize_identifier, True, "normalize_identifier"),
        "lifecycle_event": MappingRule("event_kind", lambda v: _lifecycle("APAC", v), True, "lifecycle_map"),
        "trade_id": MappingRule("trade_no", lambda v: normalize_identifier(v, "TRD-"), True, "trade_id_prefix"),
        "allocation_id": MappingRule("alloc_id", lambda v: normalize_identifier(v, "ALOC-"), False, "allocation_id_prefix"),
        "instrument_id": MappingRule("ticker", normalize_identifier, True, "normalize_identifier"),
        "instrument_id_type": MappingRule("ticker", lambda _: "RIC", True, "constant:RIC"),
        "side": MappingRule("side_flag", lambda v: _side("APAC", v), True, "side_map"),
        "quantity": MappingRule("quantity", normalize_decimal, True, "normalize_decimal"),
        "price": MappingRule("price_local", normalize_decimal, True, "normalize_decimal"),
        "currency": MappingRule("currency_code", normalize_currency, True, "normalize_currency"),
        "fx_rate_to_usd": MappingRule("fx_rate_to_usd", normalize_decimal, False, "normalize_decimal"),
        "venue": MappingRule("venue_code", _venue, True, "venue_map"),
        "account": MappingRule("acct", normalize_identifier, True, "normalize_identifier"),
        "book": MappingRule("strategy_book", normalize_identifier, True, "normalize_identifier"),
        "trade_date": MappingRule("trade_day", normalize_date, True, "normalize_date"),
        "settlement_date": MappingRule("value_date", normalize_date, False, "normalize_date"),
        "event_timestamp": MappingRule("txn_time", normalize_timestamp, True, "normalize_timestamp"),
        "sequence_number": MappingRule("event_seq", lambda v: int(v) if v is not None else None, True, "int"),
    },
}

