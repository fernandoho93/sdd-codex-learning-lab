from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from typing import Any
from urllib.parse import urlparse
from uuid import UUID, uuid4


MEDIA_TYPES = frozenset({"physical", "digital"})
GAME_STATUSES = frozenset(
    {"wishlist", "purchased", "playing", "completed", "abandoned"}
)


class GameValidationError(ValueError):
    def __init__(self, fields: dict[str, str]):
        super().__init__("Revise os campos informados.")
        self.fields = fields


class DuplicateGameError(ValueError):
    pass


class GameNotFoundError(LookupError):
    pass


@dataclass(frozen=True, slots=True)
class Game:
    id: str
    name: str
    description: str | None
    genre: str
    developer: str | None
    publisher: str | None
    release_date: str | None
    media_type: str
    status: str
    personal_rating: float | None
    cover_url: str | None
    notes: str | None
    source_name: str | None
    source_url: str | None
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_key(value: str) -> str:
    return value.strip().casefold()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def new_game(payload: dict[str, Any], *, now: str | None = None) -> Game:
    values = validate_game_payload(payload)
    timestamp = now or utc_now()
    return Game(id=str(uuid4()), created_at=timestamp, updated_at=timestamp, **values)


def updated_game(existing: Game, payload: dict[str, Any], *, now: str | None = None) -> Game:
    values = validate_game_payload(payload)
    return Game(
        id=existing.id,
        created_at=existing.created_at,
        updated_at=now or utc_now(),
        **values,
    )


def validate_game_id(value: str) -> str:
    try:
        return str(UUID(value))
    except (ValueError, TypeError, AttributeError) as error:
        raise GameNotFoundError("Jogo não encontrado.") from error


def validate_game_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise GameValidationError({"body": "O corpo deve ser um objeto JSON."})

    fields: dict[str, str] = {}
    name = _required_text(payload, "name", 200, "nome", fields)
    genre = _required_text(payload, "genre", 100, "gênero", fields)
    description = _optional_text(payload, "description", 2000, "descrição", fields)
    developer = _optional_text(payload, "developer", 200, "desenvolvedora", fields)
    publisher = _optional_text(payload, "publisher", 200, "publicadora", fields)
    notes = _optional_text(payload, "notes", 5000, "observações", fields)

    media_type = payload.get("media_type")
    if media_type not in MEDIA_TYPES:
        fields["media_type"] = "Escolha mídia física ou digital."

    status = payload.get("status")
    if status not in GAME_STATUSES:
        fields["status"] = "Escolha um status válido."

    release_date = _optional_text(payload, "release_date", 10, "lançamento", fields)
    if release_date:
        try:
            date.fromisoformat(release_date)
        except ValueError:
            fields["release_date"] = "Informe uma data válida."

    rating = payload.get("personal_rating")
    if rating in ("", None):
        rating_value = None
    elif isinstance(rating, bool) or not isinstance(rating, (int, float)):
        fields["personal_rating"] = "A nota deve ser um número entre 0 e 10."
        rating_value = None
    else:
        rating_value = float(rating)
        if not 0 <= rating_value <= 10 or not (rating_value * 2).is_integer():
            fields["personal_rating"] = "Use uma nota de 0 a 10 em passos de 0,5."

    cover_url = _optional_text(payload, "cover_url", 2048, "URL da capa", fields)
    if cover_url and not _valid_http_url(cover_url):
        fields["cover_url"] = "Informe uma URL HTTP ou HTTPS completa."

    source_name = _optional_text(payload, "source_name", 50, "fonte", fields)
    source_url = _optional_text(payload, "source_url", 2048, "URL da fonte", fields)
    if source_name or source_url:
        if source_name != "RAWG" or not source_url or not _valid_rawg_url(source_url):
            fields["source_url"] = "A atribuição externa informada é inválida."
    else:
        source_name = source_url = None

    if fields:
        raise GameValidationError(fields)

    return {
        "name": name,
        "description": description,
        "genre": genre,
        "developer": developer,
        "publisher": publisher,
        "release_date": release_date,
        "media_type": media_type,
        "status": status,
        "personal_rating": rating_value,
        "cover_url": cover_url,
        "notes": notes,
        "source_name": source_name,
        "source_url": source_url,
    }


def _required_text(
    payload: dict[str, Any], key: str, maximum: int, label: str, fields: dict[str, str]
) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        fields[key] = f"O campo {label} é obrigatório."
        return ""
    result = value.strip()
    if len(result) > maximum:
        fields[key] = f"O campo {label} aceita até {maximum} caracteres."
    return result


def _optional_text(
    payload: dict[str, Any], key: str, maximum: int, label: str, fields: dict[str, str]
) -> str | None:
    value = payload.get(key)
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        fields[key] = f"O campo {label} deve ser texto."
        return None
    result = value.strip()
    if not result:
        return None
    if len(result) > maximum:
        fields[key] = f"O campo {label} aceita até {maximum} caracteres."
    return result


def _valid_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _valid_rawg_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.hostname in {"rawg.io", "www.rawg.io"}
