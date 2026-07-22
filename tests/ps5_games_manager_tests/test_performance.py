from __future__ import annotations

import sqlite3
import time
import unittest
from pathlib import Path
from uuid import uuid4

from ps5_games_manager.repository import GameRepository


class PS5GamesPerformanceTests(unittest.TestCase):
    def test_five_thousand_games_are_listed_in_under_two_seconds(self) -> None:
        Path("tests/.tmp").mkdir(parents=True, exist_ok=True)
        path = Path("tests/.tmp") / f"performance-{uuid4()}.sqlite3"
        repository = GameRepository(path)
        rows = [(
            f"00000000-0000-4000-8000-{index:012d}", f"Game {index:04d}", f"game {index:04d}",
            "Ação", "ação", "physical", "playing", "2026-01-01T00:00:00Z", "2026-01-01T00:00:00Z",
        ) for index in range(5000)]
        with sqlite3.connect(path) as connection:
            connection.executemany(
                "INSERT INTO games (id,name,name_key,genre,genre_key,media_type,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?)",
                rows,
            )
        started = time.perf_counter()
        games = repository.list()
        elapsed = time.perf_counter() - started
        self.assertEqual(5000, len(games))
        self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
