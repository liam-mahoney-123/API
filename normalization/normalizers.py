"""Normalization helpers for cross-region post-trade events."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from typing import Any, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def json_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def normalize_identifier(value: Any, prefix: str = "") -> Optional[str]:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    normalized = raw.upper().replace(" ", "")
    return f"{prefix}{normalized}" if prefix else normalized


def normalize_currency(value: Any) -> Optional[str]:
    normalized = normalize_identifier(value)
    if normalized is None:
        return None
    return normalized[:3]


def normalize_decimal(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    raw = str(value).strip()
    if not raw:
        return None
    if "," in raw and "." in raw:
        # Handles "1,234.56" and "1.234,56".
        if raw.rfind(",") > raw.rfind("."):
            raw = raw.replace(".", "").replace(",", ".")
        else:
            raw = raw.replace(",", "")
    elif "," in raw:
        # Heuristic: treat a single comma with 3 trailing digits as thousands separator.
        left, right = raw.split(",", 1)
        if right.isdigit() and len(right) == 3 and left.replace("-", "").isdigit():
            raw = left + right
        else:
            raw = raw.replace(",", ".")
    try:
        return float(Decimal(raw))
    except (InvalidOperation, ValueError):
        return None


def _parse_datetime_string(value: str) -> Optional[datetime]:
    s = value.strip()
    if not s:
        return None
    tz_rewrites = {
        " CET": " +0100",
        " CEST": " +0200",
        " UTC": " +0000",
    }
    for suffix, replacement in tz_rewrites.items():
        if s.endswith(suffix):
            s = s[: -len(suffix)] + replacement
            break

    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%d/%m/%Y %H:%M:%S %z",
        "%Y%m%d%H%M%S",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(s, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            continue
    try:
        parsed = datetime.fromisoformat(s)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def normalize_timestamp(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        parsed = datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)
        return parsed.isoformat().replace("+00:00", "Z")
    parsed = _parse_datetime_string(str(value))
    if parsed is None:
        return None
    return parsed.isoformat().replace("+00:00", "Z")


def normalize_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, date):
        return value.isoformat()
    s = str(value).strip()
    if not s:
        return None
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y%m%d",
        "%d/%m/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None

