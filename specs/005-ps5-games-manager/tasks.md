# Tasks: PS5 Games Manager

**Input**: Design documents from `specs/005-ps5-games-manager/`

**Tests**: Required by the specification and constitution, but created only after functional implementation. Gherkin scenarios precede automated E2E.

**Organization**: Functional tasks are grouped by user story. Test tasks follow all functional stories to preserve the requested sequence.

## Phase 1: Setup

**Purpose**: Register the isolated package, runtime command, configuration and test suite boundaries.

- [x] T001 Register `ps5-games-manager` package, static assets and console command in `pyproject.toml`
- [x] T002 [P] Add PS5 database/key examples and generated-data exclusions in `.env.example` and `.gitignore`
- [x] T003 [P] Add PS5 Playwright scripts/configuration coverage in `package.json`, `tsconfig.json`, and `playwright.ps5-games-manager.config.ts`
- [x] T004 Create package and resource directories with initial modules in `src/ps5_games_manager/__init__.py`, `src/ps5_games_manager/__main__.py`, `src/ps5_games_manager/migrations/`, and `src/ps5_games_manager/web_static/`

## Phase 2: Foundational

**Purpose**: Build shared domain, persistence and HTTP foundations that block every story.

- [x] T005 Define game enums, immutable entity, input/provenance normalization, validation and domain errors in `src/ps5_games_manager/models.py`
- [x] T006 Create the versioned SQLite schema and indexes in `src/ps5_games_manager/migrations/001_create_games.sql`
- [x] T007 Implement migration execution, transactions and row mapping in `src/ps5_games_manager/repository.py`
- [x] T008 Implement shared service error mapping and CRUD orchestration foundation in `src/ps5_games_manager/service.py`
- [x] T009 Implement safe JSON routing, request limits and standardized API errors in `src/ps5_games_manager/web.py`
- [x] T010 [P] Create the semantic responsive page shell and all form fields in `src/ps5_games_manager/web_static/index.html` and `src/ps5_games_manager/web_static/app.css`
- [x] T011 Implement server startup, database path configuration and clean shutdown in `src/ps5_games_manager/__main__.py` and `src/ps5_games_manager/web.py`

**Checkpoint**: The package starts, applies migrations and serves the page/API boundary.

## Phase 3: User Story 1 - Cadastrar e consultar jogos (P1) MVP

**Goal**: Persist a valid game, list the collection and inspect complete details.

**Independent Test**: Create a required-fields-only game, restart the server, list it and open its details; invalid and duplicate submissions change nothing.

- [x] T012 [US1] Implement create, list and lookup repository operations in `src/ps5_games_manager/repository.py`
- [x] T013 [US1] Implement create, list and detail business flows including duplicate handling in `src/ps5_games_manager/service.py`
- [x] T014 [US1] Expose `POST /api/games`, `GET /api/games`, and `GET /api/games/{id}` in `src/ps5_games_manager/web.py`
- [x] T015 [US1] Implement collection loading, empty state, create form, validation messages and details in `src/ps5_games_manager/web_static/app.js`
- [x] T016 [US1] Complete collection cards, form, details and accessible state styling in `src/ps5_games_manager/web_static/index.html` and `src/ps5_games_manager/web_static/app.css`

**Checkpoint**: User Story 1 is functional and manually demonstrable after restart.

## Phase 4: User Story 2 - Pesquisar e filtrar a coleção (P2)

**Goal**: Combine partial-name search with genre and status filters.

**Independent Test**: Prepare varied games and verify each filter, combined criteria, no-results state and reset.

- [x] T017 [US2] Implement normalized search, combined filters and distinct genre lookup in `src/ps5_games_manager/repository.py` and `src/ps5_games_manager/service.py`
- [x] T018 [US2] Validate query parameters and return filter metadata from `GET /api/games` in `src/ps5_games_manager/web.py`
- [x] T019 [US2] Implement debounced search, genre/status filters, combined results and reset/no-results states in `src/ps5_games_manager/web_static/app.js`

**Checkpoint**: User Story 2 works without changing persisted records.

## Phase 5: User Story 3 - Atualizar informações e progresso (P3)

**Goal**: Edit all user fields while preserving identity, creation time and previous data on failure.

**Independent Test**: Edit status and rating, verify updated timestamp, and reject invalid/duplicate changes atomically.

- [x] T020 [US3] Implement atomic update with duplicate/not-found handling in `src/ps5_games_manager/repository.py` and `src/ps5_games_manager/service.py`
- [x] T021 [US3] Expose `PUT /api/games/{id}` with standardized responses in `src/ps5_games_manager/web.py`
- [x] T022 [US3] Implement prefilled edit mode, value preservation, loading and success/error refresh in `src/ps5_games_manager/web_static/app.js`

**Checkpoint**: User Story 3 is functional without altering ID or creation timestamp.

## Phase 6: User Story 4 - Excluir um jogo com segurança (P4)

**Goal**: Cancel or confirm definitive deletion through an accessible confirmation.

**Independent Test**: Cancel deletion and retain the game; confirm and make it unavailable from list/details.

- [x] T023 [US4] Implement atomic delete with not-found handling in `src/ps5_games_manager/repository.py` and `src/ps5_games_manager/service.py`
- [x] T024 [US4] Expose `DELETE /api/games/{id}` with empty success response in `src/ps5_games_manager/web.py`
- [x] T025 [US4] Implement accessible delete confirmation, cancellation, repeated-click guard and focus restoration in `src/ps5_games_manager/web_static/index.html`, `src/ps5_games_manager/web_static/app.js`, and `src/ps5_games_manager/web_static/app.css`

**Checkpoint**: User Story 4 is functional and cancellation performs no API mutation.

## Phase 7: User Story 5 - Preencher pelo catálogo RAWG (P5)

**Goal**: Search PS5 candidates, populate an editable form and preserve manual operation on any external failure.

**Independent Test**: Use a controlled RAWG response to populate and save a reviewed game, then simulate unavailable catalog and complete manual registration.

- [x] T026 [US5] Implement configurable RAWG client, transport boundary, PS5 mapping, HTML sanitization, persistable attribution and safe failures in `src/ps5_games_manager/rawg.py`
- [x] T027 [US5] Integrate catalog search without coupling it to local CRUD in `src/ps5_games_manager/service.py`
- [x] T028 [US5] Expose `GET /api/catalog/search` without leaking credentials or upstream URLs in `src/ps5_games_manager/web.py`
- [x] T029 [US5] Implement RAWG search, candidate selection, editable prefill, persisted attribution display and manual fallback in `src/ps5_games_manager/web_static/index.html`, `src/ps5_games_manager/web_static/app.js`, and `src/ps5_games_manager/web_static/app.css`

**Checkpoint**: All functional stories are implemented; RAWG remains optional at runtime.

## Phase 8: Integration and Manual Validation

- [x] T030 Add PS5 runtime configuration and safe defaults in `.env.example`, `src/ps5_games_manager/__main__.py`, and `src/ps5_games_manager/web.py`
- [x] T031 Run the manual CRUD, restart, filter, responsive, keyboard and RAWG fallback flows and record evidence in `specs/005-ps5-games-manager/quickstart.md`

## Phase 9: Test Scenarios and Automation

**Purpose**: Create tests only after the functional implementation, beginning with Gherkin as requested.

- [x] T032 Write the 12 minimum positive, negative and exception journeys in `specs/005-ps5-games-manager/scenarios/games-management.feature`
- [x] T033 [P] Add model validation and normalization tests in `tests/ps5_games_manager_tests/test_models.py`
- [x] T034 [P] Add migration, CRUD, uniqueness, persistence, filter and rollback tests in `tests/ps5_games_manager_tests/test_repository.py`
- [x] T035 [P] Add service rule and failure mapping tests in `tests/ps5_games_manager_tests/test_service.py`
- [x] T036 [P] Add deterministic RAWG mapping, timeout, rate-limit and malformed-response tests in `tests/ps5_games_manager_tests/test_rawg.py`
- [x] T037 Add local API contract and integration tests for all endpoints and error envelopes in `tests/ps5_games_manager_tests/test_web.py`
- [x] T038 [P] Add 5,000-record performance validation in `tests/ps5_games_manager_tests/test_performance.py`
- [x] T039 Create accessible Page Object coverage in `tests-e2e/ps5-games-manager/pages/games.page.ts`
- [x] T040 Automate the 12 Gherkin journeys, keyboard operation and mobile/desktop checks in `tests-e2e/ps5-games-manager/games.spec.ts`
- [x] T041 Run Python regression, TypeScript checking and PS5 Playwright suites and record results in `specs/005-ps5-games-manager/tasks.md`

## Phase 10: Documentation and Completion

- [x] T042 Update project overview, structure, setup, environment, database, commands, API examples, decisions, limitations and future work in `README.md`
- [x] T043 Validate every command and expected outcome in `specs/005-ps5-games-manager/quickstart.md`
- [x] T044 Verify requirement/story/task traceability and completion evidence in `specs/005-ps5-games-manager/tasks.md`

## Dependencies & Execution Order

- Phase 1 blocks all package and test configuration work.
- Phase 2 blocks every user story.
- US1 is the MVP and establishes the persisted entity and shared page flow.
- US2, US3 and US4 build on the US1 repository/service/API boundary in priority order.
- US5 depends only on the shared service/HTTP foundation and form shell, but follows local CRUD to preserve offline value.
- Manual validation follows functional implementation.
- Gherkin and automated tests follow functional implementation and precede final documentation/completion.

## Parallel Opportunities

- T002 and T003 edit independent configuration concerns.
- T010 can proceed beside backend foundational work after fields/contracts are stable.
- T033–T036 and T038 target independent test modules after implementation is complete.
- README work can begin after commands stabilize while final suites run, but completion evidence remains sequential.

## Implementation Strategy

1. Complete T001–T016 and manually demonstrate persisted create/list/detail as the MVP.
2. Add search/filter, update and deletion as separate local increments.
3. Add RAWG behind its optional adapter without changing local guarantees.
4. Perform the requested manual validation.
5. Write Gherkin, then automate domain, storage, API, external-boundary and E2E coverage.
6. Run all regression suites, validate quickstart and close traceability.

## Requirement Traceability

| Scope | Implementation tasks | Validation tasks | Result |
|---|---|---|---|
| US1 / FR-001–FR-008, FR-014–FR-018, FR-022–FR-023 | T005–T016 | T033–T037, T039–T041 | PASS |
| US2 / FR-011–FR-013, FR-019 | T017–T019 | T034–T035, T037, T040–T041 | PASS |
| US3 / FR-007–FR-008 | T020–T022 | T034–T035, T037, T040–T041 | PASS |
| US4 / FR-009–FR-010 | T023–T025 | T034–T035, T037, T040–T041 | PASS |
| US5 / FR-024–FR-030 | T026–T030 | T032, T035–T037, T040–T041 | PASS |
| NFR-001 performance | T017 | T038, T041 | PASS — 5.000 registros abaixo de 2 s |
| NFR-002–NFR-005 determinismo/integridade | T005–T029 | T033–T041 | PASS |
| NFR-006 documentação executável | T042–T043 | T043 | PASS |
| NFR-007–NFR-008 RAWG resiliente/testável | T026–T030 | T036–T037, T040–T041 | PASS |

## Completion Evidence

- 2026-07-22: checklist de especificação aprovado com 16/16 itens.
- 2026-07-22: análise cruzada encontrou e corrigiu a persistência de atribuição RAWG antes da implementação.
- 2026-07-22: instalação editável, comando `ps5-games-manager --help` e fluxo HTTP manual aprovados.
- 2026-07-22: `python -m unittest discover -s tests -v` — 56/56 aprovados.
- 2026-07-22: `npm run typecheck` — aprovado.
- 2026-07-22: `npm run test:e2e:ps5` — 30/30 aprovados em Chromium desktop e mobile.
- 2026-07-22: RAWG real não foi chamada nos testes; transporte e rotas simulados cobrem sucesso e falhas.
- 2026-07-22: quickstart e README atualizados com execução, banco, configuração, API, testes, limitações e melhorias.

