from __future__ import annotations

import sqlite3
from typing import Any

from ps5_games_manager.models import (
    GAME_STATUSES,
    DuplicateGameError,
    Game,
    GameNotFoundError,
    GameValidationError,
    new_game,
    updated_game,
    validate_game_id,
)
from ps5_games_manager.repository import GameRepository


class ServiceError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        status: int,
        fields: dict[str, str] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.fields = fields

    def to_dict(self) -> dict[str, Any]:
        error: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.fields:
            error["fields"] = self.fields
        return {"error": error}


class GameService:
    def __init__(self, repository: GameRepository, catalog: Any | None = None):
        self.repository = repository
        self.catalog = catalog

    def create(self, payload: dict[str, Any]) -> Game:
        try:
            return self.repository.add(new_game(payload))
        except GameValidationError as error:
            raise ServiceError("validation_error", str(error), status=400, fields=error.fields) from error
        except DuplicateGameError as error:
            raise ServiceError("duplicate_game", str(error), status=409) from error
        except sqlite3.Error as error:
            raise ServiceError("storage_error", "Não foi possível salvar o jogo.", status=500) from error

    def list(self, *, search: str | None = None, genre: str | None = None, status: str | None = None) -> tuple[list[Game], list[str]]:
        errors: dict[str, str] = {}
        if search is not None and len(search.strip()) > 200:
            errors["search"] = "A pesquisa aceita até 200 caracteres."
        if genre is not None and len(genre.strip()) > 100:
            errors["genre"] = "O gênero aceita até 100 caracteres."
        if status is not None and status not in GAME_STATUSES:
            errors["status"] = "Escolha um status válido."
        if errors:
            raise ServiceError("validation_error", "Revise os filtros informados.", status=400, fields=errors)
        try:
            return self.repository.list(search=search, genre=genre, status=status), self.repository.genres()
        except sqlite3.Error as error:
            raise ServiceError("storage_error", "Não foi possível consultar os jogos.", status=500) from error

    def get(self, game_id: str) -> Game:
        normalized = self._id(game_id)
        try:
            game = self.repository.get(normalized)
        except sqlite3.Error as error:
            raise ServiceError("storage_error", "Não foi possível consultar o jogo.", status=500) from error
        if game is None:
            raise ServiceError("game_not_found", "Jogo não encontrado.", status=404)
        return game

    def update(self, game_id: str, payload: dict[str, Any]) -> Game:
        existing = self.get(game_id)
        try:
            return self.repository.update(updated_game(existing, payload))
        except GameValidationError as error:
            raise ServiceError("validation_error", str(error), status=400, fields=error.fields) from error
        except DuplicateGameError as error:
            raise ServiceError("duplicate_game", str(error), status=409) from error
        except sqlite3.Error as error:
            raise ServiceError("storage_error", "Não foi possível atualizar o jogo.", status=500) from error

    def delete(self, game_id: str) -> None:
        normalized = self._id(game_id)
        try:
            deleted = self.repository.delete(normalized)
        except sqlite3.Error as error:
            raise ServiceError("storage_error", "Não foi possível excluir o jogo.", status=500) from error
        if not deleted:
            raise ServiceError("game_not_found", "Jogo não encontrado.", status=404)

    def search_catalog(self, query: str) -> dict[str, Any]:
        if not isinstance(query, str) or not query.strip() or len(query.strip()) > 200:
            raise ServiceError(
                "validation_error",
                "Informe uma pesquisa de até 200 caracteres.",
                status=400,
                fields={"query": "Informe um título para pesquisar."},
            )
        if self.catalog is None:
            raise ServiceError("catalog_not_configured", "Catálogo RAWG não configurado; continue com o cadastro manual.", status=503)
        try:
            return self.catalog.search(query.strip())
        except Exception as error:
            code = getattr(error, "code", "catalog_unavailable")
            status = 429 if code == "catalog_rate_limited" else 502
            raise ServiceError(code, str(error), status=status) from error

    @staticmethod
    def _id(value: str) -> str:
        try:
            return validate_game_id(value)
        except GameNotFoundError as error:
            raise ServiceError("game_not_found", str(error), status=404) from error
