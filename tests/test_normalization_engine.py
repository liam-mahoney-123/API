import unittest

from normalization import NormalizationEngine
from normalization.samples import get_sample_event_stream, replay_fixups


class TestNormalizationEngine(unittest.TestCase):
    def test_pipeline_publish_quarantine_dedupe_and_replay(self) -> None:
        engine = NormalizationEngine()
        results = [engine.process(event) for event in get_sample_event_stream()]

        published = [r["published"] for r in results if "published" in r]
        quarantined = [r["quarantined"] for r in results if "quarantined" in r]
        dropped = [r["dropped"] for r in results if "dropped" in r]
        buffered = [r["buffered"] for r in results if "buffered" in r]

        self.assertEqual(4, len(published))
        self.assertEqual(2, len(quarantined))
        self.assertEqual(1, len(dropped))
        self.assertEqual(1, len(buffered))
        self.assertEqual(5, len(engine.published_events()))
        self.assertEqual(2, len(engine.quarantine_snapshot()))

        replay_results = engine.replay_quarantine(replay_fixups())
        self.assertEqual(2, len(replay_results["published"]))
        self.assertEqual(7, len(engine.published_events()))
        self.assertEqual(0, len(engine.quarantine_snapshot()))

    def test_lineage_present_for_normalized_fields(self) -> None:
        engine = NormalizationEngine()
        result = engine.process(get_sample_event_stream()[0])
        self.assertIn("published", result)

        lineage = result["published"]["lineage"]
        self.assertIn("quantity", lineage)
        self.assertIn("event_timestamp", lineage)
        self.assertEqual("payload.qty", lineage["quantity"]["source_path"])
        self.assertIn("normalize_decimal", lineage["quantity"]["transforms"])

    def test_missing_required_field_goes_to_quarantine(self) -> None:
        engine = NormalizationEngine()
        result = engine.process(get_sample_event_stream()[5])
        self.assertIn("quarantined", result)
        errors = result["quarantined"]["errors"]
        self.assertTrue(any("canonical.quantity" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
