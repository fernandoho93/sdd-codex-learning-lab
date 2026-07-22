from __future__ import annotations

import json
import threading
import unittest
from pathlib import Path
from uuid import uuid4
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ps5_games_manager.rawg import RawgCatalogClient
from ps5_games_manager.web import build_server


VALID = {"name": "Astro Bot", "genre": "Plataforma", "media_type": "physical", "status": "playing"}


class PS5GamesWebTests(unittest.TestCase):
    def setUp(self) -> None:
        Path("tests/.tmp").mkdir(parents=True, exist_ok=True)
        self.server = build_server("127.0.0.1", 0, database_path=Path("tests/.tmp") / f"web-{uuid4()}.sqlite3", rawg_api_key="")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def call(self, route: str, method: str = "GET", payload: object | None = None) -> tuple[int, object | None, dict[str, str]]:
        body = json.dumps(payload).encode() if payload is not None else None
        request = Request(self.base + route, data=body, method=method, headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=3) as response:
                data = response.read()
                return response.status, json.loads(data) if data else None, dict(response.headers)
        except HTTPError as error:
            try:
                data = error.read()
                return error.code, json.loads(data) if data else None, dict(error.headers)
            finally:
                error.close()

    def create(self, **changes: object) -> dict[str, object]:
        status, body, _ = self.call("/api/games", "POST", {**VALID, **changes})
        self.assertEqual(201, status, body)
        return body  # type: ignore[return-value]

    def test_serves_page_and_assets(self) -> None:
        with urlopen(self.base + "/", timeout=3) as response:
            html = response.read().decode()
        self.assertIn("PS5 Games Manager", html)
        self.assertIn("Cadastrar jogo", html)
        with urlopen(self.base + "/assets/app.js", timeout=3) as response:
            self.assertIn("javascript", response.headers["Content-Type"])

    def test_create_list_lookup_update_delete_contract(self) -> None:
        created = self.create(personal_rating=9.5)
        self.assertIn("/api/games/", self.call("/api/games", "POST", {**VALID, "name": "Returnal"})[2]["Location"])
        status, listing, _ = self.call("/api/games?search=astro&genre=Plataforma&status=playing")
        self.assertEqual((200, 1), (status, len(listing["items"])))  # type: ignore[index]
        game_id = created["id"]
        self.assertEqual(game_id, self.call(f"/api/games/{game_id}")[1]["id"])  # type: ignore[index]
        status, updated, _ = self.call(f"/api/games/{game_id}", "PUT", {**created, "status": "completed"})
        self.assertEqual((200, "completed"), (status, updated["status"]))  # type: ignore[index]
        self.assertEqual(204, self.call(f"/api/games/{game_id}", "DELETE")[0])
        self.assertEqual(404, self.call(f"/api/games/{game_id}")[0])

    def test_validation_duplicate_and_error_envelopes(self) -> None:
        status, invalid, _ = self.call("/api/games", "POST", {})
        self.assertEqual((400, "validation_error"), (status, invalid["error"]["code"]))  # type: ignore[index]
        self.create()
        status, duplicate, _ = self.call("/api/games", "POST", {**VALID, "name": "astro bot"})
        self.assertEqual((409, "duplicate_game"), (status, duplicate["error"]["code"]))  # type: ignore[index]

    def test_invalid_json_query_and_route_are_safe(self) -> None:
        request = Request(self.base + "/api/games", data=b"{", method="POST", headers={"Content-Type": "application/json"})
        with self.assertRaises(HTTPError) as context:
            urlopen(request, timeout=3)
        self.assertEqual(400, context.exception.code)
        context.exception.close()
        self.assertEqual(400, self.call("/api/games?status=bad")[0])
        self.assertEqual(400, self.call("/api/games?unknown=x")[0])
        self.assertEqual(404, self.call("/api/missing")[0])

    def test_catalog_not_configured_is_distinct(self) -> None:
        status, body, _ = self.call("/api/catalog/search?query=Astro")
        self.assertEqual((503, "catalog_not_configured"), (status, body["error"]["code"]))  # type: ignore[index]

    def test_catalog_success_does_not_expose_key(self) -> None:
        upstream = json.dumps({"results": [{
            "id": 1, "name": "Astro Bot", "slug": "astro-bot", "released": "2024-09-06",
            "platforms": [{"platform": {"id": 187, "name": "PlayStation 5"}}], "genres": [],
        }]}).encode()
        self.server.service.catalog = RawgCatalogClient("top-secret", transport=lambda *_: (200, upstream))
        status, body, _ = self.call("/api/catalog/search?query=Astro")
        serialized = json.dumps(body)
        self.assertEqual(200, status)
        self.assertNotIn("top-secret", serialized)
        self.assertEqual("RAWG", body["items"][0]["source_name"])  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
