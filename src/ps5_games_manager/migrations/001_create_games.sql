CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    name_key TEXT NOT NULL UNIQUE,
    description TEXT,
    genre TEXT NOT NULL,
    genre_key TEXT NOT NULL,
    developer TEXT,
    publisher TEXT,
    release_date TEXT,
    media_type TEXT NOT NULL CHECK (media_type IN ('physical', 'digital')),
    status TEXT NOT NULL CHECK (status IN ('wishlist', 'purchased', 'playing', 'completed', 'abandoned')),
    personal_rating REAL CHECK (
        personal_rating IS NULL OR
        (personal_rating BETWEEN 0 AND 10 AND personal_rating * 2 = CAST(personal_rating * 2 AS INTEGER))
    ),
    cover_url TEXT,
    notes TEXT,
    source_name TEXT,
    source_url TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_games_name_key ON games(name_key);
CREATE INDEX IF NOT EXISTS idx_games_genre_key ON games(genre_key);
CREATE INDEX IF NOT EXISTS idx_games_status ON games(status);
