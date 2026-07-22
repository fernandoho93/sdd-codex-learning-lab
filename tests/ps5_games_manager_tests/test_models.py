from __future__ import annotations

import unittest

from ps5_games_manager.models import (
    GameValidationError,
    new_game,
    normalize_key,
    updated_game,
)


VALID = {
    "name": "Astro Bot",
    "genre": "Plataforma",
    "media_type": "physical",
    "status": "playing",
}


class GameModelTests(unittest.TestCase):
    def test_valid_required_fields_are_normalized(self) -> None:
        game = new_game({**VALID, "name": "  Astro Bot  ", "description": "  "}, now="2026-01-01T00:00:00Z")
        self.assertEqual("Astro Bot", game.name)
        self.assertIsNone(game.description)
        self.assertEqual(game.created_at, game.updated_at)

    def test_required_fields_are_reported_together(self) -> None:
        with self.assertRaises(GameValidationError) as context:
            new_game({})
        self.assertEqual({"name", "genre", "media_type", "status"}, set(context.exception.fields))

    def test_rating_accepts_half_steps_only(self) -> None:
        self.assertEqual(9.5, new_game({**VALID, "personal_rating": 9.5}).personal_rating)
        with self.assertRaises(GameValidationError):
            new_game({**VALID, "personal_rating": 9.7})

    def test_future_release_date_is_valid(self) -> None:
        self.assertEqual("2099-01-01", new_game({**VALID, "release_date": "2099-01-01"}).release_date)

    def test_invalid_urls_and_forged_attribution_are_rejected(self) -> None:
        with self.assertRaises(GameValidationError):
            new_game({**VALID, "cover_url": "javascript:alert(1)"})
        with self.assertRaises(GameValidationError):
            new_game({**VALID, "source_name": "RAWG", "source_url": "https://example.com/game"})

    def test_valid_rawg_attribution_is_preserved(self) -> None:
        game = new_game({**VALID, "source_name": "RAWG", "source_url": "https://rawg.io/games/astro-bot"})
        self.assertEqual("RAWG", game.source_name)

    def test_update_preserves_identity_and_creation(self) -> None:
        game = new_game(VALID, now="2026-01-01T00:00:00Z")
        updated = updated_game(game, {**VALID, "status": "completed"}, now="2026-02-01T00:00:00Z")
        self.assertEqual(game.id, updated.id)
        self.assertEqual(game.created_at, updated.created_at)
        self.assertEqual("2026-02-01T00:00:00Z", updated.updated_at)

    def test_casefold_key_ignores_case_and_outer_spaces(self) -> None:
        self.assertEqual(normalize_key(" Astro Bot "), normalize_key("astro bot"))


if __name__ == "__main__":
    unittest.main()
