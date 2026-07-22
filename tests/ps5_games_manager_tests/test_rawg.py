from __future__ import annotations

import json
import unittest
from urllib.error import URLError

from ps5_games_manager.rawg import CatalogError, RawgCatalogClient


def response_payload() -> bytes:
    return json.dumps({"results": [{
        "id": 1, "name": "Astro Bot", "slug": "astro-bot", "released": "2024-09-06",
        "background_image": "https://media.rawg.io/astro.jpg",
        "genres": [{"name": "Platformer"}], "developers": [{"name": "Team Asobi"}],
        "publishers": [{"name": "Sony"}], "description": "<p>Uma <b>aventura</b>.</p>",
        "platforms": [{"platform": {"id": 187, "name": "PlayStation 5"}}],
    }, {"id": 2, "name": "PC only", "slug": "pc-only", "platforms": [{"platform": {"id": 4, "name": "PC"}}]}]}).encode()


class RawgCatalogClientTests(unittest.TestCase):
    def test_maps_only_ps5_and_sanitizes_html(self) -> None:
        seen: list[str] = []
        client = RawgCatalogClient("secret", transport=lambda url, timeout: (seen.append(url) or 200, response_payload()))
        result = client.search("Astro")
        self.assertEqual(1, len(result["items"]))
        self.assertEqual("Uma aventura.", result["items"][0]["description"])
        self.assertEqual("RAWG", result["items"][0]["source_name"])
        self.assertIn("platforms=187", seen[0])

    def test_missing_key_does_not_call_transport(self) -> None:
        client = RawgCatalogClient("", transport=lambda *_: self.fail("transport called"))
        with self.assertRaises(CatalogError) as context:
            client.search("Astro")
        self.assertEqual("catalog_not_configured", context.exception.code)

    def test_rate_limit_has_distinct_code(self) -> None:
        with self.assertRaises(CatalogError) as context:
            RawgCatalogClient("key", transport=lambda *_: (429, b"")).search("Astro")
        self.assertEqual("catalog_rate_limited", context.exception.code)

    def test_network_failure_is_recoverable(self) -> None:
        def fail(*_args):
            raise URLError("offline")
        with self.assertRaises(CatalogError) as context:
            RawgCatalogClient("key", transport=fail).search("Astro")
        self.assertEqual("catalog_unavailable", context.exception.code)

    def test_malformed_json_is_rejected(self) -> None:
        with self.assertRaises(CatalogError):
            RawgCatalogClient("key", transport=lambda *_: (200, b"not-json")).search("Astro")


if __name__ == "__main__":
    unittest.main()
