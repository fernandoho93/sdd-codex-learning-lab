import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from prompt_lab.web import build_server


class PromptLabWebTests(unittest.TestCase):
    def setUp(self) -> None:
        test_temp = Path("tests/.tmp")
        test_temp.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=test_temp)
        data_file = Path(self.temporary.name) / "experiments.jsonl"
        self.server = build_server("127.0.0.1", 0, data_file)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_port

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temporary.cleanup()

    def request(
        self,
        method: str,
        path: str,
        payload: object | None = None,
    ) -> tuple[int, dict | str, str]:
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        body = None if payload is None else json.dumps(payload)
        headers = {} if body is None else {"Content-Type": "application/json"}
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        content_type = response.getheader("Content-Type", "")
        raw = response.read().decode("utf-8")
        connection.close()
        value = json.loads(raw) if "application/json" in content_type else raw
        return response.status, value, content_type

    def test_serves_semantic_page_and_assets(self) -> None:
        status, html, content_type = self.request("GET", "/")
        self.assertEqual(200, status)
        self.assertIn("text/html", content_type)
        self.assertIn("<title>Prompt Lab", html)
        self.assertIn('label for="prompt"', html)

        status, css, content_type = self.request("GET", "/assets/app.css")
        self.assertEqual(200, status)
        self.assertIn("text/css", content_type)
        self.assertIn(":focus-visible", css)

    def test_create_list_and_lookup_experiment(self) -> None:
        status, created, _ = self.request(
            "POST", "/api/experiments", {"prompt": "Explique SDD"}
        )
        self.assertEqual(201, status)
        self.assertEqual("Explique SDD", created["prompt"])

        status, history, _ = self.request("GET", "/api/experiments")
        self.assertEqual(200, status)
        self.assertEqual([created["id"]], [item["id"] for item in history["items"]])

        status, details, _ = self.request(
            "GET", f"/api/experiments/{created['id']}"
        )
        self.assertEqual(200, status)
        self.assertEqual(created, details)

    def test_invalid_prompt_returns_clear_bad_request(self) -> None:
        status, error, _ = self.request("POST", "/api/experiments", {"prompt": " "})
        self.assertEqual(400, status)
        self.assertIn("não pode estar vazio", error["error"])

        status, history, _ = self.request("GET", "/api/experiments")
        self.assertEqual([], history["items"])

    def test_prompt_length_boundary_matches_domain_contract(self) -> None:
        status, created, _ = self.request(
            "POST", "/api/experiments", {"prompt": "a" * 10_000}
        )
        self.assertEqual(201, status)
        self.assertEqual(10_000, len(created["prompt"]))

        status, error, _ = self.request(
            "POST", "/api/experiments", {"prompt": "a" * 10_001}
        )
        self.assertEqual(400, status)
        self.assertIn("no máximo 10.000", error["error"])

        status, history, _ = self.request("GET", "/api/experiments")
        self.assertEqual(1, len(history["items"]))

    def test_invalid_payload_and_unknown_id_are_safe(self) -> None:
        status, error, _ = self.request("POST", "/api/experiments", {"prompt": 123})
        self.assertEqual(400, status)
        self.assertIn("deve ser um texto", error["error"])

        status, error, _ = self.request("GET", "/api/experiments/inexistente")
        self.assertEqual(404, status)
        self.assertIn("não encontrado", error["error"])

    def test_unknown_route_returns_json_404(self) -> None:
        status, error, content_type = self.request("GET", "/desconhecido")
        self.assertEqual(404, status)
        self.assertIn("application/json", content_type)
        self.assertEqual("Recurso não encontrado.", error["error"])


if __name__ == "__main__":
    unittest.main()
