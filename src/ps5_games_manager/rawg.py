from __future__ import annotations

import json
from html.parser import HTMLParser
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PS5_PLATFORM_ID = 187


class CatalogError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


Transport = Callable[[str, float], tuple[int, bytes]]


class RawgCatalogClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.rawg.io/api",
        timeout: float = 5.0,
        transport: Transport | None = None,
    ):
        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transport = transport or _default_transport

    def search(self, query: str) -> dict[str, Any]:
        if not self.api_key:
            raise CatalogError("catalog_not_configured", "Catálogo RAWG não configurado; continue com o cadastro manual.")
        params = urlencode({
            "key": self.api_key,
            "search": query,
            "platforms": str(PS5_PLATFORM_ID),
            "page_size": "10",
        })
        url = f"{self.base_url}/games?{params}"
        try:
            status, body = self.transport(url, self.timeout)
        except (TimeoutError, URLError, OSError) as error:
            raise CatalogError("catalog_unavailable", "Catálogo RAWG indisponível; continue com o cadastro manual.") from error
        if status == 429:
            raise CatalogError("catalog_rate_limited", "Limite do catálogo RAWG atingido; tente novamente mais tarde.")
        if status < 200 or status >= 300:
            raise CatalogError("catalog_unavailable", "Catálogo RAWG indisponível; continue com o cadastro manual.")
        try:
            payload = json.loads(body.decode("utf-8"))
            results = payload["results"]
            if not isinstance(results, list):
                raise TypeError
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise CatalogError("catalog_unavailable", "O catálogo RAWG devolveu uma resposta inválida.") from error
        items = [candidate for item in results[:10] if (candidate := self._candidate(item))]
        return {
            "items": items,
            "attribution": {
                "text": "Dados e imagens fornecidos por RAWG",
                "url": "https://rawg.io/",
            },
        }

    @staticmethod
    def _candidate(item: Any) -> dict[str, Any] | None:
        if not isinstance(item, dict) or not _has_ps5(item):
            return None
        external_id = item.get("id")
        name = item.get("name")
        slug = item.get("slug")
        if external_id is None or not isinstance(name, str) or not name.strip() or not isinstance(slug, str) or not slug:
            return None
        genres = item.get("genres") if isinstance(item.get("genres"), list) else []
        genre = next((g.get("name") for g in genres if isinstance(g, dict) and isinstance(g.get("name"), str)), None)
        cover = item.get("background_image")
        if not isinstance(cover, str) or not cover.startswith("https://"):
            cover = None
        released = item.get("released")
        if not isinstance(released, str) or len(released) != 10:
            released = None
        return {
            "external_id": str(external_id),
            "name": name.strip()[:200],
            "description": _strip_html(item.get("description")),
            "genre": genre[:100] if genre else None,
            "developer": _company(item.get("developers")),
            "publisher": _company(item.get("publishers")),
            "release_date": released,
            "cover_url": cover,
            "source_name": "RAWG",
            "source_url": f"https://rawg.io/games/{slug}",
        }


def _default_transport(url: str, timeout: float) -> tuple[int, bytes]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "PS5GamesManager/0.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, response.read(1_000_001)
    except HTTPError as error:
        return error.code, b""


def _has_ps5(item: dict[str, Any]) -> bool:
    platforms = item.get("platforms")
    if not isinstance(platforms, list):
        return False
    for wrapper in platforms:
        platform = wrapper.get("platform") if isinstance(wrapper, dict) else None
        if isinstance(platform, dict) and (
            platform.get("id") == PS5_PLATFORM_ID or platform.get("name") == "PlayStation 5"
        ):
            return True
    return False


def _company(value: Any) -> str | None:
    if not isinstance(value, list):
        return None
    for item in value:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            return item["name"].strip()[:200] or None
    return None


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _strip_html(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    parser = _TextExtractor()
    parser.feed(value)
    text = " ".join("".join(parser.parts).split())
    return text[:2000] or None
