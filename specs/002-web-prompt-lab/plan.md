# Implementation Plan: Interface Web do Prompt Lab

**Branch**: `002-web-prompt-lab` | **Date**: 2026-07-18 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-web-prompt-lab/spec.md`

## Summary

Expor o serviço de domínio existente por um servidor HTTP local escrito com a biblioteca
padrão do Python e entregar uma página HTML/CSS/JavaScript acessível. Manter os testes de
domínio e contrato em Python; adicionar Playwright Test com TypeScript somente para jornadas
E2E no Chromium, iniciado automaticamente contra dados isolados.

## Technical Context

**Language/Version**: Python 3.11+ para aplicação; TypeScript 5.x em Node.js 20+ para E2E

**Primary Dependencies**: biblioteca padrão Python em runtime; `@playwright/test` e `typescript` em desenvolvimento

**Storage**: arquivo JSON Lines existente, com caminho configurável por ambiente

**Testing**: `unittest`, `tsc --noEmit` e Playwright Test

**Target Platform**: servidor local e Chromium headless ou interativo

**Project Type**: aplicação web local com backend Python e frontend estático

**Performance Goals**: primeira página e operações locais percebidas em até 1 segundo em ambiente de desenvolvimento

**Constraints**: offline durante execução, custo zero, sem chave, interface operável por teclado

**Scale/Scope**: um usuário local, um worker E2E e até 1.000 experimentos

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] A especificação contém histórias testáveis, priorizadas e independentes.
- [x] Servidor padrão + frontend estático é a menor arquitetura web que atende ao escopo.
- [x] Testes Python e Playwright usam apenas o provedor fake e dados locais isolados.
- [x] Segredos não são usados; dados, relatórios e traces ficam ignorados pelo Git.
- [x] Quickstart e contratos explicam API, interface e testes em linguagem direta.

**Post-design re-check**: PASS. Contratos, modelo e quickstart preservam todos os gates.

## Project Structure

### Documentation (this feature)

```text
specs/002-web-prompt-lab/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   |-- http-api.md
|   `-- web-ui.md
|-- checklists/
|   `-- requirements.md
`-- tasks.md
```

### Source Code (repository root)

```text
src/prompt_lab/
|-- web.py
`-- web_static/
    |-- index.html
    |-- app.css
    `-- app.js

tests/
`-- test_web.py

tests-e2e/
`-- prompt-lab.spec.ts

playwright.config.ts
tsconfig.json
package.json
```

**Structure Decision**: O serviço de domínio existente permanece independente. `web.py`
adapta HTTP para `PromptLabService`; arquivos estáticos usam a API no mesmo endereço.
Playwright inicia o servidor por configuração, usa um arquivo de dados próprio e executa
com um worker para preservar isolamento determinístico.

## Complexity Tracking

Não há violações constitucionais. O segundo ecossistema de desenvolvimento (Node/TypeScript)
é justificado pelo requisito explícito de aprender e executar automação E2E com Playwright;
ele não é dependência de runtime da aplicação Python.
