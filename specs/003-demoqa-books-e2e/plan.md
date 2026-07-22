# Plano de Implementação: Jornada de Livros no DemoQA

**Branch**: `003-demoqa-books-e2e` | **Date**: 2026-07-19 | **Spec**: [spec.md](spec.md)

**Input**: Especificação da feature em `specs/003-demoqa-books-e2e/spec.md`

## Summary

Criar uma suíte externa, explícita e didática para validar catálogo, pesquisa e detalhes de livros no DemoQA. A solução usa Playwright Test com TypeScript, configuração independente da aplicação local, um Page Object enxuto e três cenários autônomos executados inicialmente apenas no Chromium.

## Technical Context

**Language/Version**: TypeScript 7, com alvo ECMAScript 2022 e Node.js em modo NodeNext

**Primary Dependencies**: `@playwright/test` 1.61, `typescript` 7 e `@types/node`

**Storage**: N/A; somente artefatos efêmeros de teste em diretórios ignorados pelo Git

**Testing**: Playwright Test, asserções web com espera automática e verificação estática por `tsc --noEmit`

**Target Platform**: Navegador Chromium desktop acessando `https://demoqa.com`

**Project Type**: Suíte de testes E2E para serviço web externo

**Performance Goals**: Cada cenário deve terminar em até 30 segundos quando o serviço estiver saudável

**Constraints**: Rede externa obrigatória; serviço e dados fora do controle do projeto; sem autenticação, mutação de perfil ou dependência de publicidade; execução serial no primeiro incremento

**Scale/Scope**: 1 Page Object, 3 cenários E2E, 1 navegador e 1 livro de referência

## Constitution Check

*GATE inicial e pós-design: aprovado.*

- [x] Specification contains testable, prioritized, independent user stories.
- [x] The design is the smallest architecture that satisfies the active requirements.
- [x] Automated tests avoid paid or remote model calls and experiments are reproducible.
- [x] Secrets and generated data remain local; external AI uses a provider boundary.
- [x] A runnable quickstart and plain-language decision record are planned.

O serviço remoto acessado não é um modelo de IA e não usa segredos. A dependência externa é intencional, está isolada por comando e documentada como risco de ambiente. O plano permanece compatível com os princípios de especificação primeiro, incrementos pequenos, testes independentes e clareza educacional.

## Project Structure

### Documentation (this feature)

```text
specs/003-demoqa-books-e2e/
├── checklists/requirements.md
├── contracts/books-ui.md
├── data-model.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
playwright.config.ts                 # suíte local, limitada ao Prompt Lab
playwright.demoqa.config.ts          # suíte externa, sem servidor local
package.json                         # comandos explícitos para cada suíte
tsconfig.json                        # valida as duas configurações e os testes
tests-e2e/
├── prompt-lab.spec.ts
└── demoqa/
    ├── books.spec.ts
    └── pages/
        └── books.page.ts
```

**Structure Decision**: Manter a suíte do DemoQA dentro da estrutura TypeScript existente, mas com configuração, diretório de teste, relatório e comando próprios. O Page Object concentra somente seletores e operações reutilizadas; as expectativas de negócio continuam visíveis no arquivo de teste.

## Design Decisions

- A configuração local ganhará um `testMatch` explícito para nunca coletar a suíte externa.
- A configuração DemoQA não usará `webServer`; seu `baseURL` apontará para o site público e será acionada apenas por `test:e2e:demoqa`.
- Os seletores priorizarão papel, texto e placeholder. CSS ficará restrito a elementos sem semântica acessível adequada no site de terceiros.
- Cada teste navegará novamente para `/books`, sem compartilhar página ou estado com outros cenários.
- Captura de tela será mantida em toda falha e o trace será retido na primeira falha, inclusive sem depender de retry local.
- A primeira fase será serial e somente em Chromium para reduzir variáveis durante o aprendizado.

## Post-Design Constitution Check

- [x] As três histórias permanecem independentes e priorizadas.
- [x] Não foram introduzidas dependências de runtime nem abstrações especulativas.
- [x] Não há chamada de IA, segredo ou dado pessoal.
- [x] Evidências e relatórios são locais e ignorados pelo Git.
- [x] O quickstart explica execução, leitura do resultado e diagnóstico em linguagem simples.

## Complexity Tracking

Nenhuma violação constitucional ou complexidade excepcional foi identificada.
