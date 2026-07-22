# Plano de Implementação: API de Livros do DemoQA

**Branch**: `004-demoqa-books-api` | **Date**: 2026-07-19 | **Spec**: [spec.md](spec.md)

**Input**: Especificação da feature em `specs/004-demoqa-books-api/spec.md`

## Summary

Criar uma suíte Playwright Test com TypeScript dedicada à API pública do DemoQA. A primeira fase usa apenas a fixture isolada `request`, sem navegador, para validar catálogo, detalhe por ISBN e erro de ISBN inexistente. Configuração, comandos, relatórios e artefatos permanecem separados das suítes de interface.

## Technical Context

**Language/Version**: TypeScript 7, alvo ECMAScript 2022 e Node.js em modo NodeNext

**Primary Dependencies**: `@playwright/test` 1.61, `typescript` 7 e `@types/node`

**Storage**: N/A; apenas relatórios e anexos efêmeros ignorados pelo Git

**Testing**: Playwright Test com fixture `request`, `APIRequestContext`, asserções de contrato e `tsc --noEmit`

**Target Platform**: API REST pública `https://demoqa.com/BookStore/v1`

**Project Type**: Suíte de testes de contrato e integração HTTP externa

**Performance Goals**: Cada cenário termina em até 30 segundos quando o serviço está disponível

**Constraints**: Somente GET; sem browser, credenciais ou mutação; serviço e dados externos; execução serial; evidência JSON sem segredos

**Scale/Scope**: 3 cenários, 2 endpoints, 1 livro de referência e nenhuma instância de browser

## Constitution Check

*GATE inicial e pós-design: aprovado.*

- [x] Specification contains testable, prioritized, independent user stories.
- [x] The design is the smallest architecture that satisfies the active requirements.
- [x] Automated tests avoid paid or remote model calls and experiments are reproducible.
- [x] Secrets and generated data remain local; external AI uses a provider boundary.
- [x] A runnable quickstart and plain-language decision record are planned.

A integração externa não é um modelo de IA, não usa credenciais e é explicitamente somente leitura. O contrato remoto e o livro de referência estão documentados; os artefatos gerados permanecem ignorados pelo Git.

## Project Structure

### Documentation (this feature)

```text
specs/004-demoqa-books-api/
├── checklists/requirements.md
├── contracts/bookstore-api.md
├── data-model.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
package.json
playwright.demoqa-api.config.ts
tsconfig.json
tests-api/
└── demoqa/
    └── books-api.spec.ts
```

**Structure Decision**: Criar `tests-api/` para tornar a camada de API visível e independente de `tests-e2e/`. Uma configuração própria impede inicialização de navegador e evita que os comandos de interface coletem os testes de serviço.

## Design Decisions

- Usar a fixture `request` fornecida pelo Playwright Test; ela cria um contexto HTTP isolado por teste e respeita `baseURL` e cabeçalhos da configuração.
- Manter tipos e funções de validação no primeiro arquivo de spec para o iniciante enxergar a relação entre resposta, parsing e asserção; extrair helpers somente quando houver repetição real.
- Anexar status, cabeçalhos e corpo JSON de cada resposta ao relatório para diagnóstico, sem autenticação ou dados sensíveis.
- Validar contrato em runtime com asserções de tipo e conteúdo; interfaces TypeScript sozinhas não validam JSON recebido.
- Consultar o catálogo novamente no cenário P2 para comprovar coerência sem depender do cenário P1.
- Não configurar projeto de browser ou dispositivo, pois a fixture `request` funciona sem página.

## Post-Design Constitution Check

- [x] As histórias continuam pequenas, priorizadas e independentes.
- [x] Nenhuma dependência nova ou abstração especulativa foi introduzida.
- [x] Não há IA externa, segredo, usuário ou dado mutável.
- [x] Relatório e evidências permanecem em diretórios ignorados.
- [x] Pesquisa e quickstart explicam as decisões e a execução em linguagem didática.

## Complexity Tracking

Nenhuma violação constitucional ou complexidade excepcional foi identificada.
