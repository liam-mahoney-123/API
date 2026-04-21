"""Runnable demo for cross-region post-trade normalization."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from normalization import NormalizationEngine, get_sample_event_stream, replay_fixups


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding="utf-8")


def main() -> None:
    engine = NormalizationEngine()
    stream_result = engine.process_stream(get_sample_event_stream())

    print("=== Initial processing summary ===")
    print(json.dumps(engine.summary(), indent=2))

    print("\n=== Replaying quarantined messages ===")
    replay_result = engine.replay_quarantine(replay_fixups())
    print(json.dumps(replay_result, indent=2))

    print("\n=== Final summary ===")
    print(json.dumps(engine.summary(), indent=2))

    output_dir = Path("output")
    _write_json(output_dir / "normalized_events.json", engine.published_events())
    _write_json(output_dir / "quarantine_events.json", engine.quarantine_snapshot())
    _write_json(output_dir / "replayed_events.json", replay_result["replayed"])
    _write_json(output_dir / "initial_process_result.json", asdict(stream_result))

    print("\nWrote outputs:")
    print(f"- {output_dir / 'normalized_events.json'}")
    print(f"- {output_dir / 'quarantine_events.json'}")
    print(f"- {output_dir / 'replayed_events.json'}")
    print(f"- {output_dir / 'initial_process_result.json'}")


if __name__ == "__main__":
    main()
