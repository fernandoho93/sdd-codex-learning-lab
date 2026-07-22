# Quickstart: Interface Web e Playwright

## Preparar Python

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Preparar Playwright

```powershell
npm install
npx playwright install chromium
```

## Executar a aplicação

```powershell
prompt-lab-web --port 8000
```

Abra `http://127.0.0.1:8000`, execute um prompt, confirme o item no histórico e abra seus
detalhes. Encerre o servidor com `Ctrl+C`.

## Executar validações

```powershell
python -m unittest discover -s tests -v
npm run typecheck
npm run test:e2e
```

O Playwright inicia um servidor próprio em `127.0.0.1:8765`, usa dados sob `test-results/`
e encerra o processo ao final. Nenhum teste acessa provedor de IA externo.

## Depurar E2E

```powershell
npm run test:e2e:ui
npx playwright show-report
```

Use os locators por papel/nome do arquivo E2E para observar a ligação entre acessibilidade e
testabilidade descrita em [contracts/web-ui.md](contracts/web-ui.md).
