# Pesquisa Técnica: API de Livros do DemoQA

## Decisão 1 — Fixture HTTP isolada do Playwright

**Decision**: Usar a fixture `request` do Playwright Test em todos os cenários.

**Rationale**: A fixture fornece um `APIRequestContext` isolado por teste e aplica `baseURL` e cabeçalhos definidos na configuração. Como nenhum teste solicita `page`, o navegador não é iniciado.

**Alternatives considered**: `fetch` nativo exigiria infraestrutura própria de configuração e relatório. Associar chamadas a uma página misturaria camadas sem necessidade.

**Reference**: [Playwright API testing](https://playwright.dev/docs/api-testing)

## Decisão 2 — Configuração exclusiva da API

**Decision**: Criar `playwright.demoqa-api.config.ts`, `tests-api/demoqa/`, relatório e comando próprios.

**Rationale**: A execução permanece explícita, não inicia o Prompt Lab nem coleta cenários de UI e torna visível ao estudante qual camada está sendo testada.

**Alternatives considered**: Reutilizar a configuração DemoQA de UI reduziria um arquivo, mas manteria dispositivos, caminhos e relatórios de navegador em uma suíte que não usa browser.

## Decisão 3 — Contrato runtime e tipos TypeScript

**Decision**: Representar `Book`, `BookCollection` e `ApiError` com interfaces locais e validar os campos recebidos por asserções runtime.

**Rationale**: Fazer cast de JSON para uma interface não prova o contrato. As asserções confirmam status, conteúdo, coleção e tipos observados.

**Alternatives considered**: Introduzir uma biblioteca de schema foi rejeitado porque três contratos pequenos não justificam dependência adicional nesta fase.

## Decisão 4 — Evidência JSON anexada ao relatório

**Decision**: Anexar método, URL lógica, status, cabeçalhos e corpo de cada resposta por `testInfo.attach()`.

**Rationale**: O anexo deixa o diagnóstico reproduzível no relatório, inclusive quando a asserção posterior falha, sem depender de screenshot ou navegador.

**Alternatives considered**: `console.log` foi rejeitado por gerar saída ruidosa e pouco estruturada. Persistir arquivos manualmente duplicaria a infraestrutura do relatório.

**Reference**: [Playwright TestInfo attachments](https://playwright.dev/docs/next/api/class-testinfo)

## Decisão 5 — Contrato público observado em 2026-07-19

**Decision**: Cobrir os comportamentos observados:

- `GET /BookStore/v1/Books` → `200`, JSON e objeto com `books`;
- `GET /BookStore/v1/Book?ISBN=9781449325862` → `200` e detalhe de “Git Pocket Guide”;
- `GET /BookStore/v1/Book?ISBN=0000000000000` → `400`, código `1205` e mensagem de ISBN indisponível.

**Rationale**: Os três casos formam um MVP positivo e negativo somente leitura, diretamente verificável na documentação Swagger e no serviço público.

**Alternatives considered**: Cadastro e autenticação foram adiados porque exigem estratégia de credenciais, dados únicos e limpeza.

## Conclusão

Não restam marcações `NEEDS CLARIFICATION`. A implementação pode reutilizar as dependências já instaladas e não requer navegador ou segredo.
