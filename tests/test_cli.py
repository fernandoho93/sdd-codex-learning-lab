import io
import json
import tempfile
import unittest
from pathlib import Path

from prompt_lab.cli import main


class PromptLabCliTests(unittest.TestCase):
    def setUp(self) -> None:
        test_temp = Path("tests/.tmp")
        test_temp.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=test_temp)
        self.path = Path(self.temporary.name) / "experiments.jsonl"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = main(arguments, stdout=stdout, stderr=stderr, data_file=self.path)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_run_prints_response_and_identifier(self) -> None:
        code, output, errors = self.invoke("run", "olá")
        self.assertEqual(0, code)
        self.assertIn("Resposta: Simulação local:", output)
        self.assertIn("Experimento salvo:", output)
        self.assertEqual("", errors)

    def test_run_invalid_prompt_returns_code_two(self) -> None:
        code, output, errors = self.invoke("run", " ")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertIn("não pode estar vazio", errors)

    def test_empty_history_is_clear(self) -> None:
        code, output, _ = self.invoke("history")
        self.assertEqual(0, code)
        self.assertEqual("Nenhum experimento registrado.\n", output)

    def test_history_and_show_complete_flow(self) -> None:
        _, run_output, _ = self.invoke("run", "fluxo completo")
        identifier = run_output.split("Experimento salvo: ", 1)[1].strip()

        code, history_output, _ = self.invoke("history")
        self.assertEqual(0, code)
        self.assertIn(identifier, history_output)

        code, show_output, _ = self.invoke("show", identifier)
        self.assertEqual(0, code)
        record = json.loads(show_output)
        self.assertEqual(identifier, record["id"])
        self.assertEqual("fluxo completo", record["prompt"])

    def test_show_unknown_identifier_returns_code_two(self) -> None:
        code, output, errors = self.invoke("show", "desconhecido")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertIn("não encontrado", errors)

    def test_storage_failure_returns_code_one(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = main(
            ("run", "não pode gravar"),
            stdout=stdout,
            stderr=stderr,
            data_file=Path(self.temporary.name),
        )
        self.assertEqual(1, code)
        self.assertEqual("", stdout.getvalue())
        self.assertIn("Erro de armazenamento", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
