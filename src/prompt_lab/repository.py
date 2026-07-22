from __future__ import annotations

import json
from pathlib import Path

from prompt_lab.models import Experiment


class ExperimentRepository:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    def add(self, experiment: Experiment) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(experiment.to_dict(), ensure_ascii=False, separators=(",", ":"))
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized + "\n")

    def list_all(self) -> tuple[list[Experiment], list[str]]:
        if not self.path.exists():
            return [], []

        experiments: list[Experiment] = []
        warnings: list[str] = []
        with self.path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                    if not isinstance(value, dict):
                        raise ValueError("o registro não é um objeto")
                    experiments.append(Experiment.from_dict(value))
                except (json.JSONDecodeError, TypeError, ValueError) as error:
                    warnings.append(f"Linha {line_number} ignorada: {error}")
        return list(reversed(experiments)), warnings

    def get(self, experiment_id: str) -> tuple[Experiment | None, list[str]]:
        experiments, warnings = self.list_all()
        match = next((item for item in experiments if item.id == experiment_id), None)
        return match, warnings
