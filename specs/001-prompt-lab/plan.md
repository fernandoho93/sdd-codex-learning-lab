# Implementation Plan: Laboratório Local de Prompts

**Branch**: `001-prompt-lab` | **Date**: 2026-07-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-prompt-lab/spec.md`

## Summary

Construir uma CLI Python pequena que executa prompts por meio de um provedor simulado,
registra experimentos em JSON Lines e permite listar e inspecionar o histórico. A arquitetura
separa domínio, provedor, armazenamento e interface para que um provedor real possa ser
adicionado posteriormente sem alterar o fluxo local já testado.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: somente biblioteca padrão em runtime; `unittest` para testes

**Storage**: arquivo local JSON Lines em `data/experiments.jsonl`

**Testing**: `python -m unittest discover -s tests -v`

**Target Platform**: terminal em Windows, macOS ou Linux

**Project Type**: aplicação CLI de projeto único

**Performance Goals**: listar 1.000 registros em até 2 segundos

**Constraints**: execução offline, custo zero, nenhuma chave de API, arquivos UTF-8

**Scale/Scope**: um usuário local e até 1.000 experimentos nesta fase

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] A especificação contém histórias priorizadas, testáveis e independentes.
- [x] A CLI com biblioteca padrão é a menor arquitetura que atende aos requisitos.
- [x] Os testes usam um provedor determinístico e não acessam modelos remotos.
- [x] Segredos não são necessários e `data/` é ignorado pelo Git.
- [x] O quickstart e o guia SDD explicam execução e decisões em linguagem simples.

**Post-design re-check**: PASS. O modelo de dados, contrato e quickstart preservam os cinco gates.

## Project Structure

### Documentation (this feature)

```text
specs/001-prompt-lab/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- cli.md
|-- checklists/
|   `-- requirements.md
`-- tasks.md
```

### Source Code (repository root)

```text
src/prompt_lab/
|-- __init__.py
|-- __main__.py
|-- cli.py
|-- models.py
|-- providers.py
|-- repository.py
`-- service.py

tests/
|-- test_cli.py
|-- test_repository.py
`-- test_service.py
```

**Structure Decision**: Projeto Python único com layout `src`. O domínio não depende da CLI
nem do formato de armazenamento. `Provider` e `ExperimentRepository` são limites explícitos,
mas permanecem pequenos e concretos nesta feature.

## Complexity Tracking

Não há violações constitucionais nem complexidade que exija exceção.
