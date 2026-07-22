# Implementation Plan: PS5 Games Manager

**Branch**: `005-ps5-games-manager` | **Date**: 2026-07-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-ps5-games-manager/spec.md`

## Summary

Criar uma aplicação web local independente do Prompt Lab para gerenciar jogos de PlayStation 5.
O backend em Python expõe uma API JSON, aplica regras de domínio e persiste jogos em SQLite por
um repositório próprio. O frontend estático consome somente a API local. Um adaptador RAWG
executado no backend oferece pesquisa externa opcional, com timeout, atribuição e fallback para
cadastro manual. A implementação funcional precede a criação dos testes desta feature, conforme
a ordem solicitada, mas a conclusão continua condicionada à suíte automatizada e ao quickstart.

## Technical Context

**Language/Version**: Python 3.11+ para runtime; JavaScript moderno no navegador; TypeScript 7.x em Node.js 20+ para automação

**Primary Dependencies**: biblioteca padrão Python (`sqlite3`, `http.server`, `urllib`); `@playwright/test` e `typescript` apenas em desenvolvimento

**Storage**: SQLite local, configurável por `PS5_GAMES_DB_PATH`, com migrações SQL versionadas

**Testing**: `unittest` para domínio, persistência, API e adaptador externo; `tsc --noEmit` e Playwright para jornadas E2E

**Target Platform**: aplicação local em Windows/Linux e navegador Chromium atual

**Project Type**: aplicação web local com backend e frontend estático no mesmo pacote Python

**Performance Goals**: operações locais percebidas em até 2 segundos com 5.000 jogos; consulta externa limitada por timeout explícito

**Constraints**: um usuário, sem autenticação, CRUD offline, zero dependências Python de runtime, chave RAWG somente no servidor, testes externos determinísticos

**Scale/Scope**: uma coleção local de até 5.000 jogos, cinco histórias de usuário, um processo de servidor

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] A especificação contém histórias priorizadas, testáveis e demonstráveis de forma incremental.
- [x] A arquitetura reutiliza os padrões do repositório e adiciona somente um pacote isolado para o novo domínio.
- [x] SQLite é justificado pelas operações de atualização, exclusão, unicidade, filtros e migrações solicitadas; continua local e sem dependência externa.
- [x] A integração RAWG está isolada por um adaptador, possui timeout e não bloqueia o CRUD local.
- [x] Segredos e dados gerados permanecem fora do Git; a chave nunca chega ao navegador.
- [x] Testes automatizados usarão banco temporário e transporte RAWG simulado, sem cota, rede ou custo.
- [x] Quickstart, contratos e pesquisa registram execução e decisões em linguagem direta.

**Post-design re-check**: PASS. O modelo, os contratos e o quickstart preservam todos os gates.

## Project Structure

### Documentation (this feature)

```text
specs/005-ps5-games-manager/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   |-- games-api.md
|   |-- rawg-adapter.md
|   `-- games-web-ui.md
|-- scenarios/
|   `-- games-management.feature
|-- checklists/
|   `-- requirements.md
`-- tasks.md
```

### Source Code (repository root)

```text
src/ps5_games_manager/
|-- __init__.py
|-- __main__.py
|-- models.py
|-- repository.py
|-- service.py
|-- rawg.py
|-- web.py
|-- migrations/
|   `-- 001_create_games.sql
`-- web_static/
    |-- index.html
    |-- app.css
    `-- app.js

tests/ps5_games_manager_tests/
|-- __init__.py
|-- test_models.py
|-- test_repository.py
|-- test_service.py
|-- test_rawg.py
|-- test_web.py
`-- test_performance.py

tests-e2e/ps5-games-manager/
|-- games.spec.ts
`-- pages/
    `-- games.page.ts

playwright.ps5-games-manager.config.ts
pyproject.toml
package.json
tsconfig.json
.env.example
.gitignore
README.md
```

**Structure Decision**: Usar um pacote `src/ps5_games_manager/` separado, em vez de alterar
`src/prompt_lab/`. O pacote mantém as fronteiras já ensinadas no repositório: modelo,
repositório, serviço, adaptador HTTP e frontend estático empacotado. Testes Python ganham um
subdiretório próprio e a suíte Playwright recebe configuração e artefatos isolados.

## Architecture

```text
Browser
   |
   v
Local HTTP API ----> GameService ----> GameRepository ----> SQLite
   |
   `--------------> RawgCatalogClient ----> RAWG API (optional)
```

- `models.py` define valores, normalização e serialização sem conhecer armazenamento ou HTTP.
- `repository.py` aplica migrações e traduz registros SQLite em entidades.
- `service.py` concentra regras, validações, duplicidade e orquestração CRUD.
- `rawg.py` encapsula autenticação, timeout, mapeamento, atribuição e erros externos.
- `web.py` traduz HTTP/JSON para o serviço, sem implementar regra de negócio.
- `web_static/` mantém estado de interface e consome apenas endpoints locais.

## Implementation Phases

1. Preparar pacote, configuração, migração inicial e arquivos estáticos.
2. Implementar modelo, repositório, serviço e erros compartilhados.
3. Entregar cadastro, listagem e detalhes como primeiro corte vertical.
4. Adicionar pesquisa e filtros locais.
5. Adicionar edição e exclusão confirmada.
6. Integrar pesquisa RAWG opcional e atribuição.
7. Registrar Gherkin e então criar testes unitários, de integração e E2E.
8. Validar quickstart, atualizar README e concluir rastreabilidade.

## Complexity Tracking

| Choice | Why Needed | Simpler Alternative Rejected Because |
|--------|------------|-------------------------------------|
| SQLite em vez de JSONL | O escopo exige atualização, exclusão, unicidade transacional, filtros e migrações | Reescrever um arquivo JSONL a cada alteração aumenta risco de corrupção e duplica mecanismos já oferecidos pela biblioteca padrão |
| Adaptador RAWG opcional | O usuário solicitou API pública para preencher metadados e capas | Chamada direta no navegador exporia a chave; tornar RAWG obrigatório quebraria o requisito de CRUD local resiliente |
