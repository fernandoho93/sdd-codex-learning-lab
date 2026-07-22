from __future__ import annotations

import json
import mimetypes
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from ps5_games_manager.rawg import RawgCatalogClient
from ps5_games_manager.repository import GameRepository
from ps5_games_manager.service import GameService, ServiceError


STATIC_ROOT = Path(__file__).with_name("web_static")
STATIC_ROUTES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/assets/app.css": ("app.css", "text/css; charset=utf-8"),
    "/assets/app.js": ("app.js", "text/javascript; charset=utf-8"),
}
MAX_BODY_BYTES = 100_000


class PS5GamesHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, server_address: tuple[str, int], service: GameService):
        super().__init__(server_address, PS5GamesHandler)
        self.service = service


class PS5GamesHandler(BaseHTTPRequestHandler):
    server: PS5GamesHTTPServer

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/games":
            self._list_games(parsed.query)
            return
        if parsed.path.startswith("/api/games/"):
            self._run(lambda: self.server.service.get(self._game_id(parsed.path)), HTTPStatus.OK)
            return
        if parsed.path == "/api/catalog/search":
            self._search_catalog(parsed.query)
            return
        if parsed.path in STATIC_ROUTES:
            self._serve_static(parsed.path)
            return
        if parsed.path.startswith("/api/"):
            self._send_error(ServiceError("not_found", "Recurso não encontrado.", status=404))
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/games":
            self._send_error(ServiceError("not_found", "Recurso não encontrado.", status=404))
            return
        self._run(lambda: self.server.service.create(self._read_json()), HTTPStatus.CREATED, location=True)

    def do_PUT(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if not path.startswith("/api/games/"):
            self._send_error(ServiceError("not_found", "Recurso não encontrado.", status=404))
            return
        self._run(lambda: self.server.service.update(self._game_id(path), self._read_json()), HTTPStatus.OK)

    def do_DELETE(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if not path.startswith("/api/games/"):
            self._send_error(ServiceError("not_found", "Recurso não encontrado.", status=404))
            return
        try:
            self.server.service.delete(self._game_id(path))
            self.send_response(HTTPStatus.NO_CONTENT)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
        except ServiceError as error:
            self._send_error(error)
        except Exception:
            self._send_error(ServiceError("internal_error", "Erro interno inesperado.", status=500))

    def log_message(self, format: str, *args: Any) -> None:
        if os.environ.get("PS5_GAMES_WEB_LOG") == "1":
            super().log_message(format, *args)

    def _list_games(self, query: str) -> None:
        try:
            params = self._query(query, {"search", "genre", "status"})
            items, genres = self.server.service.list(
                search=params.get("search") or None,
                genre=params.get("genre") or None,
                status=params.get("status") or None,
            )
            self._send_json(HTTPStatus.OK, {"items": [item.to_dict() for item in items], "filters": {"genres": genres}})
        except ServiceError as error:
            self._send_error(error)
        except Exception:
            self._send_error(ServiceError("internal_error", "Erro interno inesperado.", status=500))

    def _search_catalog(self, query: str) -> None:
        try:
            params = self._query(query, {"query"})
            self._send_json(HTTPStatus.OK, self.server.service.search_catalog(params.get("query", "")))
        except ServiceError as error:
            self._send_error(error)
        except Exception:
            self._send_error(ServiceError("internal_error", "Erro interno inesperado.", status=500))

    def _run(self, action: Any, status: HTTPStatus, *, location: bool = False) -> None:
        try:
            result = action()
            headers = {"Location": f"/api/games/{result.id}"} if location else None
            self._send_json(status, result.to_dict(), headers=headers)
        except ServiceError as error:
            self._send_error(error)
        except Exception:
            self._send_error(ServiceError("internal_error", "Erro interno inesperado.", status=500))

    def _read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ServiceError("validation_error", "Tamanho de corpo inválido.", status=400) from error
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ServiceError("validation_error", "Corpo ausente ou muito grande.", status=400)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ServiceError("validation_error", "JSON inválido.", status=400) from error
        if not isinstance(payload, dict):
            raise ServiceError("validation_error", "O corpo deve ser um objeto JSON.", status=400)
        return payload

    @staticmethod
    def _query(query: str, allowed: set[str]) -> dict[str, str]:
        params = parse_qs(query, keep_blank_values=True)
        unknown = set(params) - allowed
        repeated = [key for key, values in params.items() if len(values) != 1]
        if unknown or repeated:
            raise ServiceError("validation_error", "Parâmetros de consulta inválidos.", status=400)
        return {key: values[0] for key, values in params.items()}

    @staticmethod
    def _game_id(path: str) -> str:
        value = unquote(path.removeprefix("/api/games/"))
        if not value or "/" in value:
            raise ServiceError("game_not_found", "Jogo não encontrado.", status=404)
        return value

    def _serve_static(self, route: str) -> None:
        filename, content_type = STATIC_ROUTES[route]
        try:
            content = (STATIC_ROOT / filename).read_bytes()
        except OSError:
            self._send_error(ServiceError("static_unavailable", "Interface indisponível.", status=500))
            return
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _send_error(self, error: ServiceError) -> None:
        self._send_json(HTTPStatus(error.status), error.to_dict())

    def _send_json(
        self,
        status: HTTPStatus,
        payload: object,
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content)


def build_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    *,
    database_path: Path | str | None = None,
    rawg_api_key: str | None = None,
    rawg_base_url: str | None = None,
) -> PS5GamesHTTPServer:
    database = database_path or os.environ.get("PS5_GAMES_DB_PATH", "data/ps5-games-manager.sqlite3")
    key = rawg_api_key if rawg_api_key is not None else os.environ.get("RAWG_API_KEY", "")
    catalog = None
    if key.strip():
        catalog = RawgCatalogClient(
            key,
            base_url=rawg_base_url or os.environ.get("RAWG_API_BASE_URL", "https://api.rawg.io/api"),
        )
    return PS5GamesHTTPServer((host, port), GameService(GameRepository(database), catalog))
