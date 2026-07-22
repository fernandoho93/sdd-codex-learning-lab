from __future__ import annotations

from typing import Protocol

from prompt_lab.models import ProviderResult


class Provider(Protocol):
    def generate(self, prompt: str) -> ProviderResult:
        """Generate a response without changing local experiment state."""


class FakeProvider:
    """Deterministic, offline provider used for study and automated tests."""

    name = "fake"
    model = "deterministic-study-v1"

    def generate(self, prompt: str) -> ProviderResult:
        response = f"Simulação local: recebi {len(prompt)} caracteres — {prompt}"
        return ProviderResult(
            text=response,
            provider=self.name,
            model=self.model,
            parameters={},
        )
