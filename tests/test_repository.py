import json
import tempfile
import unittest
from pathlib import Path

from prompt_lab.models import Experiment
from prompt_lab.repository import ExperimentRepository


def make_experiment(identifier: str, prompt: str = "olá") -> Experiment:
    return Experiment(
        id=identifier,
        prompt=prompt,
        response=f"resposta para {prompt}",
        provider="fake",
        model="deterministic-study-v1",
        parameters={},
        created_at=f"2026-07-16T00:00:0{identifier}+00:00",
    )


class ExperimentRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        test_temp = Path("tests/.tmp")
        test_temp.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=test_temp)
        self.path = Path(self.temporary.name) / "nested" / "experiments.jsonl"
        self.repository = ExperimentRepository(self.path)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_missing_file_is_empty_history(self) -> None:
        self.assertEqual(([], []), self.repository.list_all())
        self.assertFalse(self.path.exists())

    def test_add_preserves_unicode_and_lists_newest_first(self) -> None:
        self.repository.add(make_experiment("1", "ação"))
        self.repository.add(make_experiment("2", "coração"))
        records, warnings = self.repository.list_all()
        self.assertEqual(["2", "1"], [record.id for record in records])
        self.assertEqual("coração", records[0].prompt)
        self.assertEqual([], warnings)

    def test_corrupt_line_is_ignored_with_warning(self) -> None:
        self.path.parent.mkdir(parents=True)
        valid = json.dumps(make_experiment("1").to_dict(), ensure_ascii=False)
        self.path.write_text(f"não-json\n{valid}\n", encoding="utf-8")
        records, warnings = self.repository.list_all()
        self.assertEqual(["1"], [record.id for record in records])
        self.assertEqual(1, len(warnings))
        self.assertIn("Linha 1", warnings[0])

    def test_get_returns_record_without_changing_file(self) -> None:
        self.repository.add(make_experiment("1"))
        before = self.path.read_bytes()
        record, warnings = self.repository.get("1")
        self.assertEqual("1", record.id if record else None)
        self.assertEqual([], warnings)
        self.assertEqual(before, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
