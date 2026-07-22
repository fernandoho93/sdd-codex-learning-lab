from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from ps5_games_manager.models import DuplicateGameError, Game, normalize_key


class GameRepository:
    def __init__(self, database_path: Path | str):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._migrate()

    def add(self, game: Game) -> Game:
        values = self._database_values(game)
        columns = ", ".join(values)
        placeholders = ", ".join("?" for _ in values)
        try:
            with self._connection() as connection:
                connection.execute(
                    f"INSERT INTO games ({columns}) VALUES ({placeholders})",
                    tuple(values.values()),
                )
        except sqlite3.IntegrityError as error:
            if "name_key" in str(error) or "UNIQUE" in str(error):
                raise DuplicateGameError("Já existe um jogo com esse nome.") from error
            raise
        return game

    def list(
        self,
        *,
        search: str | None = None,
        genre: str | None = None,
        status: str | None = None,
    ) -> list[Game]:
        clauses: list[str] = []
        parameters: list[str] = []
        if search:
            clauses.append("name_key LIKE ? ESCAPE '\\'")
            escaped = normalize_key(search).replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            parameters.append(f"%{escaped}%")
        if genre:
            clauses.append("genre_key = ?")
            parameters.append(normalize_key(genre))
        if status:
            clauses.append("status = ?")
            parameters.append(status)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connection() as connection:
            rows = connection.execute(
                f"SELECT * FROM games{where} ORDER BY name_key, id", parameters
            ).fetchall()
        return [self._row_to_game(row) for row in rows]

    def genres(self) -> list[str]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT genre, genre_key FROM games GROUP BY genre_key ORDER BY genre_key"
            ).fetchall()
        return [str(row["genre"]) for row in rows]

    def get(self, game_id: str) -> Game | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM games WHERE id = ?", (game_id,)
            ).fetchone()
        return self._row_to_game(row) if row else None

    def update(self, game: Game) -> Game:
        values = self._database_values(game)
        assignments = ", ".join(f"{column} = ?" for column in values if column != "id")
        parameters = [value for column, value in values.items() if column != "id"] + [game.id]
        try:
            with self._connection() as connection:
                cursor = connection.execute(
                    f"UPDATE games SET {assignments} WHERE id = ?", parameters
                )
                if cursor.rowcount == 0:
                    return game
        except sqlite3.IntegrityError as error:
            if "name_key" in str(error) or "UNIQUE" in str(error):
                raise DuplicateGameError("Já existe um jogo com esse nome.") from error
            raise
        return game

    def delete(self, game_id: str) -> bool:
        with self._connection() as connection:
            cursor = connection.execute("DELETE FROM games WHERE id = ?", (game_id,))
            return cursor.rowcount > 0

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def _connection(self):
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _migrate(self) -> None:
        migrations = Path(__file__).with_name("migrations")
        with self._connection() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations "
                "(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
            )
            applied = {
                int(row[0])
                for row in connection.execute("SELECT version FROM schema_migrations")
            }
            for path in sorted(migrations.glob("*.sql")):
                version = int(path.stem.split("_", 1)[0])
                if version in applied:
                    continue
                connection.executescript(path.read_text(encoding="utf-8"))
                connection.execute(
                    "INSERT INTO schema_migrations (version) VALUES (?)", (version,)
                )

    @staticmethod
    def _database_values(game: Game) -> dict[str, Any]:
        values = game.to_dict()
        values["name_key"] = normalize_key(game.name)
        values["genre_key"] = normalize_key(game.genre)
        ordered = {
            "id": values["id"],
            "name": values["name"],
            "name_key": values["name_key"],
            "description": values["description"],
            "genre": values["genre"],
            "genre_key": values["genre_key"],
            "developer": values["developer"],
            "publisher": values["publisher"],
            "release_date": values["release_date"],
            "media_type": values["media_type"],
            "status": values["status"],
            "personal_rating": values["personal_rating"],
            "cover_url": values["cover_url"],
            "notes": values["notes"],
            "source_name": values["source_name"],
            "source_url": values["source_url"],
            "created_at": values["created_at"],
            "updated_at": values["updated_at"],
        }
        return ordered

    @staticmethod
    def _row_to_game(row: sqlite3.Row) -> Game:
        return Game(
            id=row["id"], name=row["name"], description=row["description"],
            genre=row["genre"], developer=row["developer"], publisher=row["publisher"],
            release_date=row["release_date"], media_type=row["media_type"], status=row["status"],
            personal_rating=row["personal_rating"], cover_url=row["cover_url"], notes=row["notes"],
            source_name=row["source_name"], source_url=row["source_url"],
            created_at=row["created_at"], updated_at=row["updated_at"],
        )
