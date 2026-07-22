from __future__ import annotations

import unittest
from pathlib import Path
from uuid import uuid4

from ps5_games_manager.models import DuplicateGameError, new_game, updated_game
from ps5_games_manager.repository import GameRepository


def payload(name: str = "Astro Bot", genre: str = "Plataforma", status: str = "playing") -> dict[str, object]:
    return {"name": name, "genre": genre, "media_type": "physical", "status": status}


class GameRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        Path("tests/.tmp").mkdir(parents=True, exist_ok=True)
        self.path = Path("tests/.tmp") / f"repository-{uuid4()}.sqlite3"
        self.repository = GameRepository(self.path)

    def test_migration_is_idempotent(self) -> None:
        GameRepository(self.path)
        self.assertEqual([], self.repository.list())

    def test_add_get_and_reopen_preserve_unicode(self) -> None:
        game = self.repository.add(new_game(payload("Demon's Souls", "Ação")))
        reopened = GameRepository(self.path)
        self.assertEqual("Ação", reopened.get(game.id).genre)

    def test_duplicate_is_case_insensitive(self) -> None:
        self.repository.add(new_game(payload("Astro Bot")))
        with self.assertRaises(DuplicateGameError):
            self.repository.add(new_game(payload(" astro bot ")))

    def test_combined_search_and_filters(self) -> None:
        self.repository.add(new_game(payload("Astro Bot", "Plataforma", "completed")))
        self.repository.add(new_game(payload("Returnal", "Ação", "playing")))
        self.assertEqual(["Astro Bot"], [g.name for g in self.repository.list(search="astro", genre="plataforma", status="completed")])

    def test_genres_are_distinct_and_ordered(self) -> None:
        self.repository.add(new_game(payload("A", "RPG")))
        self.repository.add(new_game(payload("B", "rpg")))
        self.assertEqual(["RPG"], self.repository.genres())

    def test_update_is_persisted(self) -> None:
        game = self.repository.add(new_game(payload(), now="2026-01-01T00:00:00Z"))
        changed = updated_game(game, payload(status="completed"), now="2026-02-01T00:00:00Z")
        self.repository.update(changed)
        self.assertEqual("completed", self.repository.get(game.id).status)

    def test_delete_reports_presence(self) -> None:
        game = self.repository.add(new_game(payload()))
        self.assertTrue(self.repository.delete(game.id))
        self.assertFalse(self.repository.delete(game.id))


if __name__ == "__main__":
    unittest.main()
