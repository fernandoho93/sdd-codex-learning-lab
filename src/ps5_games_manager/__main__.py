from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Sequence

from ps5_games_manager.web import build_server


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gerenciador local de jogos de PlayStation 5")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--database", type=Path)
    args = parser.parse_args(argv)
    database = args.database or Path(os.environ.get("PS5_GAMES_DB_PATH", "data/ps5-games-manager.sqlite3"))
    server = build_server(args.host, args.port, database_path=database)
    print(f"PS5 Games Manager disponível em http://{args.host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
