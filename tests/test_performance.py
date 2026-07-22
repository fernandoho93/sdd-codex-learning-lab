import json
import tempfile
import time
import unittest
from pathlib import Path

from prompt_lab.models import Experiment
from prompt_lab.repository import ExperimentRepository


class HistoryPerformanceTests(unittest.TestCase):
    def test_one_thousand_records_are_listed_in_under_two_seconds(self) -> None:
        test_temp = Path("tests/.tmp")
        test_temp.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=test_temp) as temporary:
            path = Path(temporary) / "experiments.jsonl"
            with path.open("w", encoding="utf-8") as stream:
                for index in range(1_000):
                    experiment = Experiment(
                        id=str(index),
                        prompt=f"prompt {index}",
                        response=f"resposta {index}",
                        provider="fake",
                        model="deterministic-study-v1",
                        parameters={},
                        created_at=f"2026-07-16T00:00:00.{index:06d}+00:00",
                    )
                    stream.write(json.dumps(experiment.to_dict()) + "\n")

            started = time.perf_counter()
            records, warnings = ExperimentRepository(path).list_all()
            elapsed = time.perf_counter() - started

            self.assertEqual(1_000, len(records))
            self.assertEqual([], warnings)
            self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
