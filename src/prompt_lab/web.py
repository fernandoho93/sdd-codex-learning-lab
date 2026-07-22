from __future__ import annotations

import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import unquote, urlparse

from prompt_lab.providers import FakeProvider
from prompt_lab.repository import ExperimentRepository
from prompt_lab.service import (
    ExperimentNotFoundError,
    PromptLabService,
    PromptValidationError,
)


STATIC_ROOT = Path(__file__).with_name("web_static")
STATIC_ROUTES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/assets/app.css": ("app.css", "text/css; charset=utf-8"),
    "/assets/app.js": ("app.js", "text/javascript; charset=utf-8"),
}


class PromptLabHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        service: PromptLabService,
    ) -> None:
        super().__init__(server_address, PromptLabRequestHandler)
        self.service = service


class PromptLabRequestHandler(BaseHTTPRequestHandler):
    server: PromptLabHTTPServer

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        path = urlparse(self.path).path
        if path == "/api/experiments":
            self._list_experiments()
            return
        if path.startswith("/api/experiments/"):
            experiment_id = unquote(path.removeprefix("/api/experiments/"))
            self._show_experiment(experiment_id)
            return
        if path in STATIC_ROUTES:
            filename, content_type = STATIC_ROUTES[path]
            self._serve_static(filename, content_type)
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Recurso não encontrado."})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        path = urlparse(self.path).path
        if path != "/api/experiments":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Recurso não encontrado."})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 100_000:
                raise ValueError("Corpo da requisição ausente ou muito grande.")
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            if not isinstance(payload, dict) or not isinstance(payload.get("prompt"), str):
                raise ValueError("O campo prompt deve ser um texto.")
            experiment = self.server.service.run(payload["prompt"])
            self._send_json(HTTPStatus.CREATED, experiment.to_dict())
        except PromptValidationError as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except OSError:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Não foi possível salvar o experimento."},
            )

    def log_message(self, format: str, *args: Any) -> None:
        if os.environ.get("PROMPT_LAB_WEB_LOG") == "1":
            super().log_message(format, *args)

    def _list_experiments(self) -> None:
        try:
            experiments, warnings = self.server.service.history()
            self._send_json(
                HTTPStatus.OK,
                {
                    "items": [experiment.to_dict() for experiment in experiments],
                    "warnings": warnings,
                },
            )
        except OSError:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Não foi possível consultar o histórico."},
            )

    def _show_experiment(self, experiment_id: str) -> None:
        try:
            experiment, _warnings = self.server.service.show(experiment_id)
            self._send_json(HTTPStatus.OK, experiment.to_dict())
        except ExperimentNotFoundError as error:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": str(error)})
        except OSError:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Não foi possível consultar o experimento."},
            )

    def _serve_static(self, filename: str, content_type: str) -> None:
        try:
            content = (STATIC_ROOT / filename).read_bytes()
        except OSError:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Arquivo da interface indisponível."},
            )
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, status: HTTPStatus, payload: object) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


def build_server(
    host: str = "127.0.0.1",
    port: int = 8000,
    data_file: Path | str | None = None,
) -> PromptLabHTTPServer:
    configured_path = data_file or os.environ.get(
        "PROMPT_LAB_DATA_FILE", "data/experiments.jsonl"
    )
    service = PromptLabService(FakeProvider(), ExperimentRepository(configured_path))
    return PromptLabHTTPServer((host, port), service)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Servidor web local do Prompt Lab")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    server = build_server(args.host, args.port)
    print(f"Prompt Lab disponível em http://{args.host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
