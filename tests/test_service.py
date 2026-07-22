import tempfile
import unittest
from pathlib import Path

from prompt_lab.providers import FakeProvider
from prompt_lab.repository import ExperimentRepository
from prompt_lab.service import (
    ExperimentNotFoundError,
    PromptLabService,
    PromptValidationError,
)


class PromptLabServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        test_temp = Path("tests/.tmp")
        test_temp.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=test_temp)
        self.path = Path(self.temporary.name) / "experiments.jsonl"
        self.service = PromptLabService(FakeProvider(), ExperimentRepository(self.path))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_run_normalizes_and_saves_valid_prompt(self) -> None:
        experiment = self.service.run("  explique SDD  ")
        self.assertEqual("explique SDD", experiment.prompt)
        self.assertIn("Simulação local:", experiment.response)
        records, _ = self.service.history()
        self.assertEqual([experiment], records)

    def test_empty_prompt_is_rejected_without_file(self) -> None:
        with self.assertRaises(PromptValidationError):
            self.service.run("   ")
        self.assertFalse(self.path.exists())

    def test_too_long_prompt_is_rejected(self) -> None:
        with self.assertRaises(PromptValidationError):
            self.service.run("a" * 10_001)

    def test_history_is_newest_first(self) -> None:
        first = self.service.run("primeiro")
        second = self.service.run("segundo")
        records, _ = self.service.history()
        self.assertEqual([second.id, first.id], [record.id for record in records])

    def test_show_finds_record(self) -> None:
        saved = self.service.run("mostrar")
        found, warnings = self.service.show(saved.id)
        self.assertEqual(saved, found)
        self.assertEqual([], warnings)

    def test_show_rejects_unknown_identifier(self) -> None:
        with self.assertRaises(ExperimentNotFoundError):
            self.service.show("inexistente")


if __name__ == "__main__":
    unittest.main()
