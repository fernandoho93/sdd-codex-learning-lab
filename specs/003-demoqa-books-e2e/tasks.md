# Tasks: Jornada de Livros no DemoQA

**Input**: Documentos de design em `specs/003-demoqa-books-e2e/`

**Tests**: Obrigatórios pela constituição e pelo pedido do usuário. Cada história entrega um cenário E2E independente.

## Phase 1: Setup

**Purpose**: Separar de forma explícita as suítes local e externa.

- [x] T001 Restringir a coleta da suíte local ao Prompt Lab em playwright.config.ts
- [x] T002 [P] Incluir a configuração externa nos arquivos validados em tsconfig.json
- [x] T003 Criar configuração Chromium exclusiva do DemoQA com evidências isoladas em playwright.demoqa.config.ts
- [x] T004 Adicionar comandos explícitos de execução, depuração e relatório do DemoQA em package.json

## Phase 2: Foundational

**Purpose**: Criar a fronteira reutilizável da página e o dado de teste conhecido.

- [x] T005 Criar o Page Object com navegação, pesquisa, resultados e detalhes em tests-e2e/demoqa/pages/books.page.ts

**Checkpoint**: A suíte externa pode navegar e consultar elementos sem compartilhar estado com a suíte local.

## Phase 3: User Story 1 - Consultar o catálogo de livros (P1) MVP

**Goal**: Abrir o catálogo e reconhecer sua estrutura, pesquisa e livro conhecido.

**Independent Test**: Executar apenas o cenário de catálogo e confirmar os três elementos essenciais.

- [x] T006 [US1] Criar o cenário independente de disponibilidade do catálogo em tests-e2e/demoqa/books.spec.ts
- [x] T007 [US1] Executar e estabilizar o cenário P1 contra o DemoQA em tests-e2e/demoqa/books.spec.ts

## Phase 4: User Story 2 - Pesquisar um livro (P2)

**Goal**: Validar pesquisa correspondente, estado vazio e restauração.

**Independent Test**: Executar somente o cenário de pesquisa e observar as três transições sem depender do cenário P1.

- [x] T008 [US2] Adicionar pesquisa positiva, termo inexistente e limpeza em tests-e2e/demoqa/books.spec.ts
- [x] T009 [US2] Executar e estabilizar o cenário P2 contra o DemoQA em tests-e2e/demoqa/books.spec.ts

## Phase 5: User Story 3 - Consultar detalhes de um livro (P3)

**Goal**: Abrir o livro conhecido, validar dados essenciais e retornar ao catálogo.

**Independent Test**: Executar somente o cenário de detalhes e verificar título, autor, ISBN e retorno.

- [x] T010 [US3] Adicionar navegação, validação de detalhes e retorno em tests-e2e/demoqa/books.spec.ts
- [x] T011 [US3] Executar e estabilizar o cenário P3 contra o DemoQA em tests-e2e/demoqa/books.spec.ts

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T012 [P] Documentar escopo, comandos e trilha de evolução do DemoQA em README.md
- [x] T013 Executar verificação TypeScript com npm run typecheck
- [x] T014 Executar a suíte externa completa com npm run test:e2e:demoqa
- [x] T015 Executar as regressões local E2E e Python com npm run test:e2e e python -m unittest discover -s tests -v
- [x] T016 Validar os comandos e resultados descritos em specs/003-demoqa-books-e2e/quickstart.md
- [x] T017 Registrar conclusão e rastreabilidade de FR-001 a FR-010 em specs/003-demoqa-books-e2e/tasks.md

## Dependencies & Execution Order

- T001-T004 preparam o isolamento e bloqueiam a execução externa.
- T005 fornece operações compartilhadas para todas as histórias.
- US1 é o MVP e valida a conexão e o contrato mínimo do catálogo.
- US2 e US3 são cenários independentes depois de T005, embora sejam implementados em ordem didática P1 → P2 → P3.
- A validação final depende das três histórias concluídas.

## Parallel Opportunities

- T002 pode ser executada em paralelo com T001 porque modifica outro arquivo.
- T012 pode ser preparada em paralelo com os cenários porque modifica somente README.md.
- Depois do Page Object, US2 e US3 são conceitualmente independentes; a ordem serial foi escolhida para favorecer o estudo incremental.

## Implementation Strategy

Concluir T001-T007 e executar somente o catálogo como MVP. Em seguida, acrescentar pesquisa e detalhes, executando cada cenário isoladamente antes da suíte completa. Encerrar com verificação estática, regressões e quickstart.

## Requirement Traceability

| Requisito | Cobertura planejada |
|---|---|
| FR-001, FR-002 | US1 / T006-T007 |
| FR-003, FR-004, FR-005 | US2 / T008-T009 |
| FR-006, FR-007 | US3 / T010-T011 |
| FR-008 | Reinicialização em cada teste no books.spec.ts |
| FR-009 | Configuração de screenshot, trace e relatório em T003 |
| FR-010 | Configurações e comandos separados em T001-T004 |

## Completion Evidence

- `npm run typecheck`: aprovado em 2026-07-19.
- `npm run test:e2e:demoqa`: 3/3 cenários aprovados no Chromium em 38,3 segundos.
- `npm run test:e2e`: 5/5 regressões locais aprovadas.
- `python -m unittest discover -s tests -v`: 24/24 testes aprovados.
- Os cenários P1, P2 e P3 também foram executados isoladamente antes da suíte completa.
- O diagnóstico inicial preservou screenshot e trace e revelou mudanças reais no contrato público do DemoQA; seletores e documentos foram sincronizados antes da conclusão.
