# Pesquisa Técnica: Jornada de Livros no DemoQA

## Decisão 1 — Configuração externa separada

**Decision**: Criar `playwright.demoqa.config.ts`, com `baseURL` externo, diretório e artefatos próprios; restringir a configuração atual ao teste local.

**Rationale**: O teste do DemoQA exige internet e não deve iniciar o servidor Python do Prompt Lab. Configurações distintas deixam custo, dependência e intenção explícitos. O Playwright permite definir `testDir`, `testMatch`, `baseURL`, projetos e artefatos por configuração.

**Alternatives considered**: Uma única configuração com todos os testes foi rejeitada porque misturaria ambiente local e externo. Projetos em uma mesma configuração foram considerados, mas ainda tornariam o comando padrão menos didático nesta primeira fase.

**Reference**: [Playwright TestConfig](https://playwright.dev/docs/api/class-testconfig)

## Decisão 2 — Seletores próximos da percepção do usuário

**Decision**: Priorizar `getByRole`, `getByPlaceholder` e `getByText`; encapsular CSS apenas onde o DemoQA não expõe semântica adequada.

**Rationale**: Localizadores orientados ao usuário tornam o teste legível, recebem espera automática e tendem a representar melhor o contrato percebido. Como não controlamos o HTML do DemoQA, um pequeno Page Object isola exceções inevitáveis.

**Alternatives considered**: XPath e cadeias CSS profundas foram rejeitados por acoplarem o teste à estrutura visual interna. Adicionar `data-testid` não é possível em um site de terceiros.

**Reference**: [Playwright Locators](https://playwright.dev/docs/locators)

## Decisão 3 — Page Object mínimo

**Decision**: Usar uma única classe `BooksPage` para navegação, pesquisa, linhas do catálogo e detalhes.

**Rationale**: O objeto elimina repetição e ensina separação entre “como operar a página” e “o que o cenário comprova”, sem criar camadas extras.

**Alternatives considered**: Escrever tudo no spec seria aceitável para um único teste, mas repetiria seletores nos três incrementos. Fixtures personalizadas foram adiadas até existir necessidade real de preparação compartilhada.

**Reference**: [Playwright Fixtures e Page Objects](https://playwright.dev/docs/test-fixtures)

## Decisão 4 — Evidências na primeira falha

**Decision**: Capturar screenshot somente em falha e reter trace na primeira falha; gerar relatório HTML separado.

**Rationale**: Uma falha externa precisa mostrar DOM, ações, rede e imagem imediatamente. `retain-on-first-failure` conserva o trace da execução original e não exige uma repetição para produzir diagnóstico.

**Alternatives considered**: `on-first-retry` economiza artefatos, porém exigiria retry local para gerar trace. Vídeo contínuo foi adiado porque aumenta armazenamento sem necessidade atual.

**Reference**: [Playwright TestOptions](https://playwright.dev/docs/api/class-testoptions)

## Decisão 5 — Dado de teste conhecido e explícito

**Decision**: Usar “Git Pocket Guide”, autor “Richard E. Silverman” e ISBN “9781449325862” como dados legíveis no cenário.

**Rationale**: O iniciante consegue relacionar entrada e resultado sem fixture opaca. Como o catálogo pertence ao DemoQA, a suposição e o custo de manutenção ficam documentados.

**Alternatives considered**: Escolher dinamicamente o primeiro livro reduziria dependência do título, mas enfraqueceria as expectativas e poderia mascarar alterações de dados.

## Conclusão

Não restam marcações `NEEDS CLARIFICATION`. A solução é pequena, separa ambientes e possui evidência adequada para investigar instabilidade externa.
