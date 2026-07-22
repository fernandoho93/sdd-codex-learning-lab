# Tasks: API de Livros do DemoQA

**Input**: Documentos de design em `specs/004-demoqa-books-api/`

**Tests**: Obrigatórios pela constituição e pelo pedido do usuário. Cada história entrega um teste HTTP independente.

## Phase 1: Setup

**Purpose**: Criar uma suíte HTTP externa explícita e separada das interfaces.

- [x] T001 Criar configuração exclusiva sem projeto de browser em playwright.demoqa-api.config.ts
- [x] T002 [P] Incluir configuração e testes de API na verificação estática em tsconfig.json
- [x] T003 Adicionar comandos de execução, modo UI e relatório da API em package.json

## Phase 2: Foundational

**Purpose**: Definir tipos, dado de referência, validação runtime e evidência reutilizada.

- [x] T004 Criar contratos TypeScript, livro de referência e anexo de resposta em tests-api/demoqa/books-api.spec.ts

**Checkpoint**: A suíte pode realizar requisições isoladas e registrar respostas sem iniciar navegador.

## Phase 3: User Story 1 - Consultar o catálogo pela API (P1) MVP

**Goal**: Validar status, conteúdo JSON, coleção, campos essenciais e livro conhecido.

**Independent Test**: Executar somente `API-US1` e confirmar o contrato do catálogo sem depender de outro cenário.

- [x] T005 [US1] Implementar cenário de contrato do catálogo em tests-api/demoqa/books-api.spec.ts
- [x] T006 [US1] Executar e estabilizar API-US1 contra o DemoQA em tests-api/demoqa/books-api.spec.ts

## Phase 4: User Story 2 - Consultar um livro por ISBN (P2)

**Goal**: Validar o detalhe conhecido e sua coerência com o catálogo.

**Independent Test**: Executar somente `API-US2`, consultando catálogo e detalhe dentro do próprio teste.

- [x] T007 [US2] Implementar cenário independente de detalhe e coerência em tests-api/demoqa/books-api.spec.ts
- [x] T008 [US2] Executar e estabilizar API-US2 contra o DemoQA em tests-api/demoqa/books-api.spec.ts

## Phase 5: User Story 3 - Rejeitar ISBN inexistente (P3)

**Goal**: Validar status 400, código 1205 e mensagem do contrato negativo.

**Independent Test**: Executar somente `API-US3` com ISBN reservado inexistente.

- [x] T009 [US3] Implementar cenário negativo de ISBN inexistente em tests-api/demoqa/books-api.spec.ts
- [x] T010 [US3] Executar e estabilizar API-US3 contra o DemoQA em tests-api/demoqa/books-api.spec.ts

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T011 [P] Documentar camada, comandos e ordem de estudo da API em README.md
- [x] T012 Executar verificação TypeScript com npm run typecheck
- [x] T013 Executar a suíte completa com npm run test:api:demoqa
- [x] T014 Executar regressões Python, E2E local e E2E DemoQA com os comandos documentados em README.md
- [x] T015 Validar os comandos e resultados de specs/004-demoqa-books-api/quickstart.md
- [x] T016 Registrar conclusão e rastreabilidade de FR-001 a FR-011 em specs/004-demoqa-books-api/tasks.md

## Dependencies & Execution Order

- T001-T003 preparam coleta, tipos e comandos e bloqueiam a execução.
- T004 fornece contratos e evidência para as três histórias.
- US1 é o MVP e comprova o endpoint de coleção.
- US2 e US3 são independentes depois de T004; a ordem P1 → P2 → P3 é didática.
- Validação final depende dos três cenários concluídos.

## Parallel Opportunities

- T002 pode ocorrer em paralelo com T001 porque modifica outro arquivo.
- T011 pode ser preparada em paralelo com os cenários porque modifica apenas README.md.
- US2 e US3 são conceitualmente independentes após T004, embora compartilhem o mesmo spec e devam ser editadas sequencialmente.

## Implementation Strategy

Concluir T001-T006 e executar o catálogo como MVP. Acrescentar detalhe e erro em incrementos separados, sempre executando primeiro o cenário isolado. Encerrar com suíte completa, regressões, quickstart e rastreabilidade.

## Requirement Traceability

| Requisito | Cobertura planejada |
|---|---|
| FR-001 a FR-004 | US1 / T005-T006 |
| FR-005 e FR-006 | US2 / T007-T008 |
| FR-007 e FR-008 | US3 / T009-T010 |
| FR-009 | Fixture isolada e GET em T004-T010 |
| FR-010 | Configuração e comandos próprios em T001-T003 |
| FR-011 | Anexo estruturado de resposta em T004 |

## Completion Evidence

- `npm run typecheck`: aprovado em 2026-07-19.
- `npm run test:api:demoqa`: 3/3 testes aprovados no projeto `api-demoqa` em 3,3 segundos.
- `npm run test:e2e`: 5/5 regressões locais aprovadas.
- `npm run test:e2e:demoqa`: 3/3 regressões externas de interface aprovadas.
- `python -m unittest discover -s tests -v`: 24/24 testes aprovados.
- API-US1, API-US2 e API-US3 também foram executados isoladamente antes da suíte completa.
- A descoberta por configuração confirmou isolamento: 3 testes API, 5 testes E2E locais e 3 testes E2E DemoQA.
- Cada resposta HTTP foi anexada ao relatório como JSON com recurso, status, cabeçalhos e corpo.
