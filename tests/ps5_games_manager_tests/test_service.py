from __future__ import annotations

import unittest
from pathlib import Path
from uuid import uuid4

from ps5_games_manager.repository import GameRepository
from ps5_games_manager.service import GameService, ServiceError


VALID = {"name": "Astro Bot", "genre": "Plataforma", "media_type": "physical", "status": "playing"}


class GameServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        Path("tests/.tmp").mkdir(parents=True, exist_ok=True)
        self.service = GameService(GameRepository(Path("tests/.tmp") / f"service-{uuid4()}.sqlite3"))

    def test_complete_crud_flow(self) -> None:
        game = self.service.create(VALID)
        self.assertEqual(game, self.service.get(game.id))
        changed = self.service.update(game.id, {**VALID, "status": "completed"})
        self.assertEqual("completed", changed.status)
        self.service.delete(game.id)
        with self.assertRaises(ServiceError) as context:
            self.service.get(game.id)
        self.assertEqual("game_not_found", context.exception.code)

    def test_validation_error_has_fields(self) -> None:
        with self.assertRaises(ServiceError) as context:
            self.service.create({})
        self.assertEqual(400, context.exception.status)
        self.assertIn("name", context.exception.fields)

    def test_duplicate_has_conflict_code(self) -> None:
        self.service.create(VALID)
        with self.assertRaises(ServiceError) as context:
            self.service.create({**VALID, "name": "astro bot"})
        self.assertEqual((409, "duplicate_game"), (context.exception.status, context.exception.code))

    def test_invalid_filters_are_rejected(self) -> None:
        with self.assertRaises(ServiceError) as context:
            self.service.list(status="unknown")
        self.assertEqual("validation_error", context.exception.code)

    def test_catalog_not_configured_preserves_local_service(self) -> None:
        with self.assertRaises(ServiceError) as context:
            self.service.search_catalog("Astro")
        self.assertEqual((503, "catalog_not_configured"), (context.exception.status, context.exception.code))
        self.assertEqual("Astro Bot", self.service.create(VALID).name)


if __name__ == "__main__":
    unittest.main()
