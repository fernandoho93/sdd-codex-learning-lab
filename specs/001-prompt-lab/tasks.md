# Tasks: Laboratório Local de Prompts

**Input**: Design documents from `specs/001-prompt-lab/`

**Tests**: Required by the constitution. All provider tests use the deterministic fake.

## Phase 1: Setup

**Purpose**: Criar a base instalável e segura do projeto.

- [x] T001 Initialize the Python package metadata in pyproject.toml
- [x] T002 [P] Configure Python, secret, and generated-data exclusions in .gitignore
- [x] T003 [P] Document setup and SDD learning flow in README.md and docs/SDD-GUIDE.md

## Phase 2: Foundational

**Purpose**: Criar os limites compartilhados usados por todas as histórias.

- [x] T004 Create immutable Experiment and ProviderResult models in src/prompt_lab/models.py
- [x] T005 [P] Create the deterministic provider boundary in src/prompt_lab/providers.py
- [x] T006 Implement JSON Lines persistence and corruption warnings in src/prompt_lab/repository.py
- [x] T007 [P] Add repository unit tests in tests/test_repository.py

**Checkpoint**: Domínio, provedor e persistência prontos para as histórias.

## Phase 3: User Story 1 - Executar um experimento local (P1) MVP

**Goal**: Validar um prompt, produzir resposta local e salvar o experimento.

**Independent Test**: Um prompt válido gera e salva exatamente um registro; entrada inválida não grava nada.

- [x] T008 [P] [US1] Add service tests for valid and invalid prompts in tests/test_service.py
- [x] T009 [US1] Implement prompt validation and experiment execution in src/prompt_lab/service.py
- [x] T010 [P] [US1] Add run-command tests in tests/test_cli.py
- [x] T011 [US1] Implement the run command and exit codes in src/prompt_lab/cli.py

## Phase 4: User Story 2 - Consultar o histórico (P2)

**Goal**: Listar experimentos do mais recente para o mais antigo.

**Independent Test**: Dois registros aparecem em ordem inversa de criação; histórico vazio é informativo.

- [x] T012 [P] [US2] Add history service and CLI tests in tests/test_service.py and tests/test_cli.py
- [x] T013 [US2] Implement history listing in src/prompt_lab/service.py and src/prompt_lab/cli.py

## Phase 5: User Story 3 - Inspecionar um experimento (P3)

**Goal**: Recuperar todos os dados de um registro por identificador.

**Independent Test**: Um ID existente mostra o registro; um ID desconhecido não altera o arquivo.

- [x] T014 [P] [US3] Add show service and CLI tests in tests/test_service.py and tests/test_cli.py
- [x] T015 [US3] Implement experiment lookup in src/prompt_lab/service.py and src/prompt_lab/cli.py

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T016 [P] Add package entry points in src/prompt_lab/__init__.py and src/prompt_lab/__main__.py
- [x] T017 Validate the runnable scenarios in specs/001-prompt-lab/quickstart.md
- [x] T018 Run the full test suite and record completion in specs/001-prompt-lab/tasks.md
- [x] T019 Add the 1,000-record performance criterion test in tests/test_performance.py
- [x] T020 Add deterministic provider coverage in tests/test_providers.py
- [x] T021 Add storage-failure CLI coverage in tests/test_cli.py

## Dependencies & Execution Order

- Setup blocks all implementation.
- Foundational blocks US1, US2, and US3.
- US1 is the suggested MVP.
- US2 and US3 depend only on the foundation and can be developed independently after it.
- Polish follows the selected user stories.

## Parallel Opportunities

- T002 and T003 touch different files.
- T005 and T007 can proceed after T004's model contract is known.
- Test tasks marked `[P]` can be written before their implementation tasks.

## Implementation Strategy

Complete T001-T011 first and validate the MVP. Then add history and inspection as separate,
independently testable increments. Keep the fake provider when a real provider is introduced
later so the existing test suite remains deterministic and free.
