# Quickstart: Testes E2E do DemoQA Books

## Objetivo

Executar separadamente os cenários externos de catálogo, pesquisa e detalhes sem iniciar a aplicação local do Prompt Lab.

## Pré-requisitos

- Node.js e dependências do projeto instalados com `npm install`.
- Chromium do Playwright instalado com `npx playwright install chromium`.
- Acesso à internet para `https://demoqa.com/books`.

## Executar

```powershell
npm run typecheck
npm run test:e2e:demoqa
```

Resultado esperado: três testes aprovados no projeto `chromium-demoqa`.

## Entender os três testes

1. **Catálogo**: abre `/books` e verifica a coluna de títulos, a pesquisa e um livro conhecido.
2. **Pesquisa**: valida resultado correspondente, resultado vazio e restauração do catálogo.
3. **Detalhes**: abre o livro conhecido, confere título, autor e ISBN e retorna.

Cada teste abre a página novamente. Assim, uma falha não deixa estado para o próximo cenário.

## Modo visual e depuração

```powershell
npm run test:e2e:demoqa:ui
npm run test:e2e:demoqa:debug
```

O modo UI ajuda a acompanhar passos e localizar elementos. O modo debug abre o Inspector e pausa a execução para análise.

## Relatório

```powershell
npm run report:e2e:demoqa
```

Em uma falha, consulte primeiro a mensagem da asserção, depois a captura de tela e o trace no relatório. Como o alvo é externo, confirme também se o DemoQA está acessível antes de alterar o teste.

## Executar somente a suíte local

```powershell
npm run test:e2e
```

Esse comando continua executando apenas o Prompt Lab local e não acessa o DemoQA.
