# Quickstart: Testes da API DemoQA Books

## Objetivo

Executar três testes HTTP públicos — catálogo, detalhe e ISBN inexistente — sem abrir navegador e sem iniciar o Prompt Lab.

## Pré-requisitos

- Node.js e dependências instaladas com `npm install`.
- Acesso à internet para `https://demoqa.com`.
- Não é necessário instalar ou abrir navegador para esta suíte.

## Executar

```powershell
npm run typecheck
npm run test:api:demoqa
```

Resultado esperado: três testes aprovados no projeto `api-demoqa`.

## O que cada teste ensina

1. **Catálogo**: GET, status 200, `Content-Type`, parsing JSON, array e campos obrigatórios.
2. **Detalhe**: query string, livro conhecido e coerência entre duas respostas.
3. **Erro**: status 400, código de domínio e mensagem útil.

## Modo UI e relatório

```powershell
npm run test:api:demoqa:ui
npm run report:api:demoqa
```

O modo UI mostra os testes e os passos, mesmo sem página de navegador. No relatório, cada teste contém um anexo JSON com status, cabeçalhos e corpo da resposta.

## Executar um único cenário

```powershell
npx playwright test --config=playwright.demoqa-api.config.ts --grep "API-US1:"
```

## Diagnóstico

Se um teste falhar:

1. leia a asserção que falhou;
2. abra o anexo JSON da resposta no relatório;
3. confirme se `https://demoqa.com/swagger` e o endpoint estão disponíveis;
4. compare a resposta atual com `contracts/bookstore-api.md`;
5. se o serviço mudou legitimamente, atualize primeiro especificação e contrato.

## Limite de escopo

Esta suíte é somente leitura. Não crie usuário, token ou massa pública até existir uma nova feature SDD com estratégia explícita de criação e limpeza.
