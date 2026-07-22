# Prompt Lab SDD

Projeto didático para aprender desenvolvimento orientado por especificações (SDD)
enquanto construímos, em etapas pequenas, um laboratório de experimentos com IA.

## O que você vai aprender

Neste repositório, a ordem de trabalho é deliberada:

1. **Constituição**: define regras que todas as features precisam respeitar.
2. **Especificação**: descreve o problema, o valor para o usuário e os critérios de aceite.
3. **Plano**: decide a arquitetura e as tecnologias.
4. **Tarefas**: transforma o plano em passos pequenos e rastreáveis.
5. **Análise**: compara especificação, plano e tarefas para encontrar lacunas.
6. **Implementação**: escreve código e testes seguindo as tarefas.

Os artefatos da primeira feature estão em
[`specs/001-prompt-lab`](specs/001-prompt-lab/).

Os artefatos da interface web e da automação E2E estão em
[`specs/002-web-prompt-lab`](specs/002-web-prompt-lab/).

Os artefatos do estudo E2E em um site externo estão em
[`specs/003-demoqa-books-e2e`](specs/003-demoqa-books-e2e/).

Os artefatos dos testes da API pública de livros estão em
[`specs/004-demoqa-books-api`](specs/004-demoqa-books-api/).

## Primeiro MVP

O primeiro incremento é um laboratório de prompts executado no terminal. Ele usa um
provedor simulado e determinístico: não envia dados à internet e não exige chave de API.
Isso permite estudar o fluxo SDD, testes, persistência e separação de responsabilidades
antes de adicionar custos e riscos de uma integração real.

## Preparação do ambiente

Requisitos:

- Python 3.11 ou superior
- Git
- PowerShell no Windows

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Execute os testes:

```powershell
python -m unittest discover -s tests -v
```

Execute o laboratório:

```powershell
prompt-lab run "Explique o que é SDD em três frases"
prompt-lab history
```

Execute a interface web:

```powershell
prompt-lab-web --port 8000
```

Abra `http://127.0.0.1:8000` no navegador. O servidor reutiliza o mesmo domínio, provedor
simulado e histórico da CLI.

Por padrão, os experimentos ficam em `data/experiments.jsonl`. Essa pasta é local e
ignorada pelo Git.

## Como estudar este repositório

Leia nesta ordem:

1. [Constituição](.specify/memory/constitution.md)
2. [Especificação da feature](specs/001-prompt-lab/spec.md)
3. [Plano técnico](specs/001-prompt-lab/plan.md)
4. [Modelo de dados](specs/001-prompt-lab/data-model.md)
5. [Contrato da CLI](specs/001-prompt-lab/contracts/cli.md)
6. [Tarefas](specs/001-prompt-lab/tasks.md)
7. Código em `src/prompt_lab/` e testes em `tests/`

Para estudar a segunda feature, repita a mesma ordem dentro de
`specs/002-web-prompt-lab/` e depois leia `tests-e2e/prompt-lab.spec.ts`.

Para estudar a terceira feature, repita a ordem em
`specs/003-demoqa-books-e2e/`, leia o Page Object em
`tests-e2e/demoqa/pages/books.page.ts` e depois os cenários em
`tests-e2e/demoqa/books.spec.ts`.

Para estudar a quarta feature, leia `specs/004-demoqa-books-api/` e depois
`tests-api/demoqa/books-api.spec.ts`. Observe como cada requisito do contrato HTTP
vira uma asserção de status, cabeçalho ou corpo.

## Testes Playwright com TypeScript

Prepare as dependências de desenvolvimento uma vez:

```powershell
npm install
npx playwright install chromium
```

Execute as três camadas de validação:

```powershell
python -m unittest discover -s tests -v
npm run typecheck
npm run test:e2e
```

- `unittest` protege domínio, persistência, CLI e contrato HTTP.
- `tsc --noEmit` valida os tipos da automação.
- Playwright valida formulário, mensagens, histórico e detalhes em um Chromium real.

Para acompanhar visualmente ou depurar:

```powershell
npm run test:e2e:ui
npm run test:e2e:debug
npm run report:e2e
```

Observe a rastreabilidade: histórias `US1`, requisitos `FR-001` e tarefas `T001`
mostram por que cada parte existe.

## Estudo E2E com DemoQA Books

O alvo externo é `https://demoqa.com/books`. Essa página funciona como catálogo,
pesquisa e consulta de detalhes; ela não possui carrinho, checkout ou pagamento.
Neste primeiro incremento também não usamos login nem alteramos dados públicos.

Execute somente a suíte externa:

```powershell
npm run typecheck
npm run test:e2e:demoqa
```

Para acompanhar ou depurar:

```powershell
npm run test:e2e:demoqa:ui
npm run test:e2e:demoqa:debug
npm run report:e2e:demoqa
```

A suíte percorre três passos de aprendizado: disponibilidade do catálogo, pesquisa
com e sem resultado e navegação para detalhes. Cada cenário começa novamente em
`/books`, portanto não depende da ordem dos testes. Como o DemoQA é externo, uma
falha também pode representar indisponibilidade ou mudança do site; use o screenshot
e o trace do relatório antes de alterar a automação.

## Testes da API DemoQA Books

A camada de API usa a fixture HTTP isolada do Playwright e não abre navegador. O
primeiro incremento é somente leitura: catálogo, detalhe por ISBN e ISBN inexistente.

```powershell
npm run typecheck
npm run test:api:demoqa
```

Para acompanhar os passos e abrir o relatório com as respostas anexadas:

```powershell
npm run test:api:demoqa:ui
npm run report:api:demoqa
```

Os testes de API complementam os testes E2E: a API valida o contrato HTTP de forma
rápida e direta; a interface valida o comportamento percebido por uma pessoa.

## Próximos incrementos sugeridos

- integrar um provedor real de modelos em uma nova feature;
- comparar duas respostas para o mesmo prompt;
- registrar tokens, latência e custo estimado;
- evoluir o DemoQA para paginação, ordenação e cenários autenticados em features separadas.

## Segurança

- Nunca coloque chaves de API no código ou no Git.
- Copie `.env.example` para `.env` apenas quando uma integração real for adicionada.
- Não envie dados pessoais, confidenciais ou de clientes a um modelo durante os estudos.
- Trate respostas de modelos como conteúdo não confiável, não como fatos.

## PS5 Games Manager

O PS5 Games Manager é uma aplicação web local para cadastrar e acompanhar uma coleção pessoal
de jogos de PlayStation 5. Ele oferece cadastro, listagem, detalhes, edição, exclusão confirmada,
pesquisa por nome, filtros por gênero/status e preenchimento opcional pelo catálogo RAWG.

### Tecnologias e decisões

- Python 3.11+ e biblioteca padrão no backend.
- SQLite local com migração SQL versionada e unicidade normalizada de nomes.
- HTML semântico, CSS responsivo e JavaScript sem framework no frontend.
- RAWG opcional, consultada somente pelo backend com chave em variável de ambiente.
- `unittest` para domínio, banco, serviço, API e fronteira RAWG.
- Playwright/TypeScript para jornadas reais em Chromium desktop e mobile.

O CRUD não depende da RAWG. Falha, ausência de chave ou limite da fonte externa mantém o
cadastro manual disponível. Dados e imagens externos preservam atribuição e vínculo para RAWG.

### Estrutura

```text
src/ps5_games_manager/                  backend e frontend estático
tests/ps5_games_manager_tests/          testes Python
tests-e2e/ps5-games-manager/            testes Playwright
specs/005-ps5-games-manager/            especificação, plano, contratos e tarefas
playwright.ps5-games-manager.config.ts  ambiente E2E isolado
```

### Instalação e execução

Requisitos: Python 3.11+, Node.js 20+ para testes E2E e uma chave RAWG somente se a pesquisa
externa for desejada.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
npm install
ps5-games-manager --port 8080
```

Abra `http://127.0.0.1:8080`. Backend, API e frontend são entregues pelo mesmo processo.

### Configuração e banco

```powershell
$env:PS5_GAMES_DB_PATH = 'data/minha-colecao.sqlite3'
$env:RAWG_API_KEY = 'sua-chave-local-opcional'
ps5-games-manager --port 8080
```

- `PS5_GAMES_DB_PATH`: caminho do SQLite; padrão `data/ps5-games-manager.sqlite3`.
- `RAWG_API_KEY`: habilita a pesquisa pública; nunca deve ser versionada.
- `PS5_GAMES_WEB_LOG=1`: habilita log HTTP local para diagnóstico.

Arquivos SQLite, `.env`, relatórios, traces e dados gerados são ignorados pelo Git. A migração
`src/ps5_games_manager/migrations/001_create_games.sql` é aplicada automaticamente.

### API local

```powershell
Invoke-RestMethod http://127.0.0.1:8080/api/games

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8080/api/games `
  -ContentType 'application/json' `
  -Body '{"name":"Astro Bot","genre":"Plataforma","media_type":"physical","status":"playing"}'

Invoke-RestMethod 'http://127.0.0.1:8080/api/games?search=astro&status=playing'
Invoke-RestMethod 'http://127.0.0.1:8080/api/catalog/search?query=Astro%20Bot'
```

O contrato completo, incluindo atualização, exclusão e erros padronizados, está em
[`specs/005-ps5-games-manager/contracts/games-api.md`](specs/005-ps5-games-manager/contracts/games-api.md).

### Testes

```powershell
python -m unittest discover -s tests -v
npm run typecheck
npm run test:e2e:ps5
```

O Playwright inicia servidor e banco exclusivos sob `test-results/`; a RAWG real não é chamada.
Para depuração e relatório:

```powershell
npm run test:e2e:ps5:ui
npm run report:e2e:ps5
```

### Limitações e melhorias futuras

- O MVP atende uma pessoa em uma instalação local, sem autenticação ou sincronização.
- A exclusão é definitiva e não há importação em lote, paginação ou upload de capas.
- A RAWG requer chave, internet e atribuição; seus resultados são sugestões editáveis.
- Melhorias futuras incluem backup/exportação, ordenação configurável, paginação, cache externo
  compatível com os termos do provedor e suporte opcional a múltiplas plataformas.
