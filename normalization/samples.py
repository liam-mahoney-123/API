"""Representative regional sample payloads and replay patches."""

from __future__ import annotations

from typing import Any


def get_sample_event_stream() -> list[dict[str, Any]]:
    """Raw events with intentionally divergent regional schemas."""
    return [
        # US event (flat schema + epoch ms timestamp).
        {
            "region": "US",
            "payload": {
                "eventId": "US-1001",
                "msgType": "EXEC",
                "side": "B",
                "eventTimeMs": 1713703200123,
                "tradeDate": "2026-04-21",
                "symbol": "AAPL",
                "tradeRef": "TRD-AAPL-20260421-001",
                "mic": "XNAS",
                "qty": "1,500",
                "px": "173.42",
                "ccy": "usd",
                "accountId": "ac-001",
                "book": "EQT_US_LONGLONG",
                "allocRef": "ALOC-991",
                "seqNum": 1,
                "fxRate": "1.0",
            },
            "metadata": {"source_system": "us_oms", "ingest_channel": "kafka-us"},
        },
        # APAC event (different field names + day-first timestamp with timezone).
        {
            "region": "APAC",
            "payload": {
                "msg_id": "AP-9001",
                "event_kind": "BOOK",
                "side_flag": "1",
                "trade_no": "AP-TRD-700HK-42",
                "txn_time": "21/04/2026 15:00:01 +0800",
                "trade_day": "20260421",
                "ticker": "700 HK",
                "venue_code": "SEHK",
                "quantity": "2,000",
                "price_local": "312.5",
                "currency_code": "HKD",
                "acct": " hk_alpha_12 ",
                "strategy_book": "ASIA_GROWTH",
                "alloc_id": "A-HK-22",
                "event_seq": 2,
                "fx_rate_to_usd": "0.1282",
            },
            "metadata": {"source_system": "apac_posttrade", "ingest_channel": "mq-apac"},
        },
        # EU event (different lifecycle code + CET text timestamp).
        {
            "region": "EMEA",
            "payload": {
                "id": "EU-4433",
                "lifecycle": "CXL",
                "side_code": "SELL",
                "trade_ref": "EU-TRD-4433",
                "timestamp": "2026-04-21 09:35:22 CET",
                "biz_date": "21-04-2026",
                "isin": "US5949181045",
                "venue": "XLON",
                "shares": "500",
                "price": "255.11",
                "currency": "GBP",
                "book_code": " UK_EQ_CORE ",
                "acct_num": "uk-prime-01",
                "sequence": 1,
            },
            "metadata": {"source_system": "emea_middle", "ingest_channel": "sftp-emea"},
        },
        # Duplicate message id.
        {
            "region": "US",
            "payload": {
                "eventId": "US-1001",
                "msgType": "EXEC",
                "side": "B",
                "eventTimeMs": 1713703200123,
                "tradeDate": "2026-04-21",
                "symbol": "AAPL",
                "tradeRef": "TRD-AAPL-20260421-001",
                "mic": "XNAS",
                "qty": "1500",
                "px": "173.42",
                "ccy": "USD",
                "accountId": "ac-001",
                "book": "EQT_US_LONGLONG",
                "allocRef": "ALOC-991",
                "seqNum": 1,
            },
            "metadata": {"source_system": "us_oms", "ingest_channel": "kafka-us"},
        },
        # APAC lower sequence arrives after higher sequence: sequencing issue.
        {
            "region": "APAC",
            "payload": {
                "msg_id": "AP-9002",
                "event_kind": "BOOK",
                "side_flag": "1",
                "trade_no": "AP-TRD-700HK-42",
                "txn_time": "21/04/2026 15:02:01 +0800",
                "trade_day": "20260421",
                "ticker": "700 HK",
                "venue_code": "SEHK",
                "quantity": "500",
                "price_local": "313.1",
                "currency_code": "HKD",
                "acct": "hk_alpha_12",
                "strategy_book": "ASIA_GROWTH",
                "alloc_id": "A-HK-22",
                "event_seq": 1,
            },
            "metadata": {"source_system": "apac_posttrade", "ingest_channel": "mq-apac"},
        },
        # Missing required quantity -> quarantine.
        {
            "region": "EMEA",
            "payload": {
                "id": "EU-5000",
                "lifecycle": "NEW",
                "side_code": "BUY",
                "trade_ref": "EU-TRD-5000",
                "timestamp": "2026-04-21 10:00:00 CET",
                "biz_date": "21-04-2026",
                "isin": "GB00BH4HKS39",
                "venue": "XLON",
                "price": "102.05",
                "currency": "GBP",
                "book_code": "UK_EQ_CORE",
                "acct_num": "uk-prime-02",
                "sequence": 1,
            },
            "metadata": {"source_system": "emea_middle", "ingest_channel": "sftp-emea"},
        },
        # Unsupported region -> quarantine.
        {
            "region": "LATAM",
            "payload": {
                "id_local": "LAT-100",
                "type": "DONE",
                "time_local": "2026-04-21T13:00:00-03:00",
                "symbol_local": "PETR4",
            },
            "metadata": {"source_system": "latam_legacy", "ingest_channel": "file-drop"},
        },
        # Late-arriving event (older event timestamp but higher sequence).
        {
            "region": "US",
            "payload": {
                "eventId": "US-1002",
                "msgType": "CORR",
                "side": "B",
                "eventTimeMs": 1713703100123,
                "tradeDate": "2026-04-21",
                "symbol": "AAPL",
                "tradeRef": "TRD-AAPL-20260421-001",
                "mic": "XNAS",
                "qty": "1500",
                "px": "173.50",
                "ccy": "USD",
                "accountId": "ac-001",
                "book": "EQT_US_LONGLONG",
                "allocRef": "ALOC-991",
                "seqNum": 2,
            },
            "metadata": {
                "source_system": "us_oms",
                "ingest_channel": "kafka-us",
                "arrived_late": True,
            },
        },
    ]


def replay_fixups() -> list[dict[str, Any]]:
    """Patches for messages that were quarantined in the initial run."""
    return [
        {
            "quarantine_id": "EMEA:EU-5000",
            "payload_patch": {"shares": "750"},
            "replay_metadata": {"operator": "ops_user_1", "reason": "Filled missing shares"},
        },
        {
            "quarantine_id": "LATAM:LAT-100",
            "payload_patch": {
                "region_override": "US",
                "eventId": "LAT-100",
                "msgType": "EXEC",
                "side": "S",
                "eventTimeMs": 1713704400000,
                "tradeDate": "2026-04-21",
                "symbol": "PETR4",
                "mic": "BVMF",
                "qty": "1000",
                "px": "6.71",
                "ccy": "BRL",
                "accountId": "br-crossbook-1",
                "book": "LATAM_EQ",
                "tradeRef": "TRD-PETR4-20260421-001",
                "seqNum": 1,
            },
            "replay_metadata": {"operator": "ops_user_2", "reason": "Re-mapped unsupported source"},
        },
    ]
