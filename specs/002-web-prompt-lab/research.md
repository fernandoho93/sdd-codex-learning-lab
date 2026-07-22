# Research: Interface Web do Prompt Lab

## Servidor HTTP da biblioteca padrão

**Decision**: usar `ThreadingHTTPServer` e um handler pequeno.

**Rationale**: a feature possui três endpoints locais e arquivos estáticos; um framework
adicionaria conceitos e dependências sem resolver uma necessidade atual.

**Alternatives considered**: FastAPI e Flask são apropriados para APIs maiores, mas ficam
adiados até surgirem requisitos de validação, middleware ou implantação externa.

## Frontend estático sem framework

**Decision**: HTML semântico, CSS e JavaScript modular simples.

**Rationale**: mantém foco em jornadas, acessibilidade e testes E2E, sem pipeline de build do
produto. TypeScript permanece restrito aos testes solicitados.

**Alternatives considered**: React/Vue aumentariam dependências e duplicariam complexidade
para um formulário, uma lista e um painel de detalhes.

## Playwright Test com TypeScript

**Decision**: usar `@playwright/test`, configuração TypeScript, Chromium e `tsc --noEmit`.

**Rationale**: fornece locators acessíveis, assertions aguardáveis, trace e relatório HTML.
TypeScript é suportado diretamente, enquanto a checagem separada impede erros de tipos ocultos.

**Alternatives considered**: Playwright Python reduziria linguagens, mas não atenderia ao
objetivo de estudo em TypeScript; Cypress criaria outra escolha sem benefício para este escopo.

## Estratégia de testes

**Decision**: manter regras em Python e testar somente jornadas críticas no navegador.

**Rationale**: evita uma pirâmide invertida. Playwright prova integração real entre página,
HTTP, domínio e persistência; `unittest` continua responsável por limites e falhas detalhadas.

**Alternatives considered**: reproduzir todos os casos de borda no navegador seria mais lento,
mais frágil e não aumentaria proporcionalmente a confiança.
