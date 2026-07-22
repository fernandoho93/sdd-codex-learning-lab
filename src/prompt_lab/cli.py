from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Sequence, TextIO

from prompt_lab.providers import FakeProvider
from prompt_lab.repository import ExperimentRepository
from prompt_lab.service import (
    ExperimentNotFoundError,
    PromptLabService,
    PromptValidationError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-lab",
        description="Laboratório local e determinístico para estudar prompts e SDD.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    run_parser = commands.add_parser("run", help="executa e salva um prompt")
    run_parser.add_argument("prompt")
    commands.add_parser("history", help="lista experimentos")
    show_parser = commands.add_parser("show", help="mostra um experimento")
    show_parser.add_argument("id")
    return parser


def create_service(data_file: Path | str | None = None) -> PromptLabService:
    configured_path = data_file or os.environ.get(
        "PROMPT_LAB_DATA_FILE", "data/experiments.jsonl"
    )
    return PromptLabService(FakeProvider(), ExperimentRepository(configured_path))


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    data_file: Path | str | None = None,
) -> int:
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        service = create_service(data_file)

        if args.command == "run":
            experiment = service.run(args.prompt)
            print(f"Resposta: {experiment.response}", file=output)
            print(f"Experimento salvo: {experiment.id}", file=output)
            return 0

        if args.command == "history":
            experiments, warnings = service.history()
            _print_warnings(warnings, errors)
            if not experiments:
                print("Nenhum experimento registrado.", file=output)
                return 0
            for experiment in experiments:
                summary = experiment.prompt[:60].replace("\n", " ")
                print(f"{experiment.id} | {experiment.created_at} | {summary}", file=output)
            return 0

        experiment, warnings = service.show(args.id)
        _print_warnings(warnings, errors)
        print(json.dumps(experiment.to_dict(), ensure_ascii=False, indent=2), file=output)
        return 0
    except (PromptValidationError, ExperimentNotFoundError) as error:
        print(f"Erro: {error}", file=errors)
        return 2
    except OSError as error:
        print(f"Erro de armazenamento: {error}", file=errors)
        return 1


def _print_warnings(warnings: list[str], stream: TextIO) -> None:
    for warning in warnings:
        print(f"Aviso: {warning}", file=stream)
