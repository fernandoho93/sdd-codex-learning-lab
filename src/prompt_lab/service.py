from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from prompt_lab.models import Experiment
from prompt_lab.providers import Provider
from prompt_lab.repository import ExperimentRepository


class PromptValidationError(ValueError):
    pass


class ExperimentNotFoundError(LookupError):
    pass


class PromptLabService:
    def __init__(self, provider: Provider, repository: ExperimentRepository) -> None:
        self.provider = provider
        self.repository = repository

    def run(self, prompt: str) -> Experiment:
        normalized = prompt.strip()
        if not normalized:
            raise PromptValidationError("O prompt não pode estar vazio.")
        if len(normalized) > 10_000:
            raise PromptValidationError("O prompt deve ter no máximo 10.000 caracteres.")

        result = self.provider.generate(normalized)
        experiment = Experiment(
            id=str(uuid4()),
            prompt=normalized,
            response=result.text,
            provider=result.provider,
            model=result.model,
            parameters=result.parameters,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.repository.add(experiment)
        return experiment

    def history(self) -> tuple[list[Experiment], list[str]]:
        return self.repository.list_all()

    def show(self, experiment_id: str) -> tuple[Experiment, list[str]]:
        experiment, warnings = self.repository.get(experiment_id)
        if experiment is None:
            raise ExperimentNotFoundError(f"Experimento não encontrado: {experiment_id}")
        return experiment, warnings
