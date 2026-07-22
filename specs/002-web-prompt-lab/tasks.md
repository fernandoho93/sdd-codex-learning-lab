# Tasks: Interface Web do Prompt Lab

**Input**: Design documents from `specs/002-web-prompt-lab/`

**Tests**: Required by the constitution. Browser tests use only the local fake provider.

## Phase 1: Setup

**Purpose**: Preparar os dois ambientes de desenvolvimento sem alterar o domínio existente.

- [x] T001 Create Playwright and TypeScript development metadata in package.json, tsconfig.json, and playwright.config.ts
- [x] T002 [P] Add Node, Playwright report, trace, and test-data exclusions to .gitignore
- [x] T003 [P] Add the web console entry point and static package data to pyproject.toml

## Phase 2: Foundational

**Purpose**: Expor domínio e arquivos estáticos por uma fronteira HTTP testável.

- [x] T004 Add HTTP API contract tests for create, list, lookup, validation, and static files in tests/test_web.py
- [x] T005 Implement the local HTTP server and JSON API adapter in src/prompt_lab/web.py
- [x] T006 [P] Create the semantic page shell in src/prompt_lab/web_static/index.html
- [x] T007 [P] Create responsive accessible styles in src/prompt_lab/web_static/app.css

**Checkpoint**: API e página base podem ser iniciadas localmente.

## Phase 3: User Story 1 - Executar um prompt no navegador (P1) MVP

**Goal**: Executar um prompt válido e comunicar sucesso ou erro pela página.

**Independent Test**: Preencher, executar e verificar resposta, ID e estado acessível; prompt vazio mostra erro.

- [x] T008 [P] [US1] Add valid, invalid, and keyboard execution scenarios in tests-e2e/prompt-lab.spec.ts
- [x] T009 [US1] Implement prompt validation, loading, API submission, and result rendering in src/prompt_lab/web_static/app.js
- [x] T010 [US1] Align accessible names and live regions with the UI contract in src/prompt_lab/web_static/index.html

## Phase 4: User Story 2 - Consultar histórico na página (P2)

**Goal**: Mostrar estado vazio e inserir novos experimentos no topo.

**Independent Test**: Um prompt único aparece no histórico sem reload e pode ser localizado por nome acessível.

- [x] T011 [P] [US2] Add empty and updated history scenarios in tests-e2e/prompt-lab.spec.ts
- [x] T012 [US2] Implement history loading, empty state, warnings, and refresh in src/prompt_lab/web_static/app.js

## Phase 5: User Story 3 - Inspecionar detalhes no navegador (P3)

**Goal**: Abrir metadados reproduzíveis de um item do histórico.

**Independent Test**: Selecionar item e verificar todos os campos em região focável.

- [x] T013 [P] [US3] Add experiment details scenario in tests-e2e/prompt-lab.spec.ts
- [x] T014 [US3] Implement detail lookup, rendering, focus, and recoverable errors in src/prompt_lab/web_static/app.js

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T015 [P] Document web and E2E commands in README.md
- [x] T016 [P] Add deterministic test scripts and single-worker browser configuration in package.json and playwright.config.ts
- [x] T017 Install Node development dependencies and Chromium using package-lock.json and local Playwright cache
- [x] T018 Run Python regression and HTTP tests with python -m unittest discover -s tests -v
- [x] T019 Run TypeScript verification with npm run typecheck
- [x] T020 Run Chromium E2E tests and report generation with npm run test:e2e
- [x] T021 Validate all quickstart scenarios in specs/002-web-prompt-lab/quickstart.md
- [x] T022 Record completion and requirement traceability in specs/002-web-prompt-lab/tasks.md

## Dependencies & Execution Order

- Setup blocks all TypeScript and installed-server validation.
- Foundational blocks browser user stories.
- US1 is the MVP and proves the full vertical slice.
- US2 and US3 build independently on the shared HTTP/history foundation after US1.
- Final validation requires all selected stories.

## Parallel Opportunities

- T002 and T003 touch independent configuration files.
- T006 and T007 can proceed after the HTTP static contract is defined.
- E2E scenarios marked `[P]` can be authored before their JavaScript implementation.
- T015 and T016 update separate documentation/configuration concerns.

## Implementation Strategy

Complete T001-T010 and run the P1 Playwright scenario first. Then add history and details as
separate slices. Keep Python unit/API tests as the broad regression layer and a deliberately
small browser suite for user-visible journeys.
