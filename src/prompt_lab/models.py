from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ProviderResult:
    text: str
    provider: str
    model: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Experiment:
    id: str
    prompt: str
    response: str
    provider: str
    model: str
    parameters: dict[str, Any]
    created_at: str
    status: str = "completed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Experiment:
        required = {
            "id",
            "prompt",
            "response",
            "provider",
            "model",
            "parameters",
            "created_at",
            "status",
        }
        missing = required.difference(value)
        if missing:
            raise ValueError(f"Campos ausentes: {', '.join(sorted(missing))}")
        if not isinstance(value["parameters"], dict):
            raise ValueError("O campo parameters deve ser um objeto")
        return cls(**{key: value[key] for key in required})
