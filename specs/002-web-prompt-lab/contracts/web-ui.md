# Web UI Contract

## Formulário

- Campo multilinha com nome acessível `Prompt` e contador de até 10.000 caracteres.
- Botão `Executar prompt` associado ao formulário.
- Durante envio, botão desabilitado e texto `Executando...`.
- Resultado e erros anunciados por uma região viva.

## Resultado

- Título `Resultado`.
- Resposta completa.
- Texto `Experimento salvo` acompanhado pelo identificador.

## Histórico

- Título `Histórico`.
- Estado vazio `Nenhum experimento registrado.`.
- Cada item é um botão com nome contendo o resumo do prompt.
- Novo experimento entra no topo sem recarregar a página.

## Detalhes

- Título `Detalhes do experimento`.
- Campos: ID, prompt, resposta, provedor, modelo, data UTC e estado.
- A região recebe foco programático quando aberta para usuários de teclado.
