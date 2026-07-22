# Quickstart: PS5 Games Manager

## Prerequisites

- Python 3.11+
- Node.js 20+ somente para TypeScript e Playwright
- Chave RAWG opcional para pesquisa pública

## Prepare

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
npm install
```

Opcionalmente copie `.env.example` para `.env` e disponibilize a chave no ambiente. O projeto
não carrega `.env` automaticamente para evitar nova dependência:

```powershell
$env:RAWG_API_KEY = 'sua-chave-local'
```

## Run

```powershell
ps5-games-manager --port 8080
```

Abra `http://127.0.0.1:8080`. Por padrão, o banco fica em
`data/ps5-games-manager.sqlite3`. Para outro caminho:

```powershell
$env:PS5_GAMES_DB_PATH = 'data/minha-colecao.sqlite3'
ps5-games-manager --port 8080
```

## Manual validation

1. Confirme o estado vazio e cadastre um jogo válido.
2. Reinicie o servidor e confirme que o jogo permanece disponível.
3. Abra detalhes e edite status/nota.
4. Crie outros jogos e combine pesquisa, gênero e status.
5. Tente nome duplicado com capitalização diferente.
6. Cancele uma exclusão e depois confirme a remoção.
7. Com `RAWG_API_KEY`, pesquise um jogo, aplique os dados, revise e salve.
8. Sem a chave, confirme que a falha RAWG não bloqueia o cadastro manual.
9. Repita os fluxos em 360 px e somente com teclado.

## Automated validation

Os cenários Gherkin são registrados antes dos testes. Depois da implementação funcional:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
npm run typecheck
npm run test:e2e:ps5
```

O Playwright inicia servidor e banco isolados sob `test-results/`. Testes não acessam RAWG real.

## API examples

```powershell
Invoke-RestMethod http://127.0.0.1:8080/api/games

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8080/api/games `
  -ContentType 'application/json' `
  -Body '{"name":"Astro Bot","genre":"Plataforma","media_type":"physical","status":"playing"}'

Invoke-RestMethod 'http://127.0.0.1:8080/api/games?search=astro&status=playing'
```

Consulte [contracts/games-api.md](contracts/games-api.md) para o contrato completo.

## Validation evidence

Validado em 2026-07-22 no Windows:

- instalação editável e comando `ps5-games-manager` disponíveis;
- fluxo HTTP manual com criação, listagem, duplicidade, edição, pesquisa/filtro, RAWG não
  configurada e exclusão;
- `python -m unittest discover -s tests -v`: 56 testes aprovados;
- `npm run typecheck`: aprovado;
- `npm run test:e2e:ps5`: 30 testes aprovados em Chromium desktop e mobile;
- pesquisa RAWG positiva validada por transporte/rota simulados e determinísticos, sem chave real.

Os testes E2E validam também teclado, formulário responsivo em viewport móvel, confirmação e
cancelamento de exclusão, mensagens de erro e continuidade do cadastro manual sem RAWG.
