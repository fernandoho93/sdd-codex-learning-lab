# Data Model: Interface Web do Prompt Lab

## Experiment

A entidade existente é reutilizada sem alterações. A API serializa os mesmos campos definidos
em `specs/001-prompt-lab/data-model.md`.

## ExecutionState

Estado somente da interface, não persistido.

| Estado | Entrada | Saída permitida |
|---|---|---|
| `idle` | página pronta | `loading` |
| `loading` | envio de prompt | `success` ou `error` |
| `success` | resposta válida | `loading` |
| `error` | erro validado ou operacional | `loading` |

Durante `loading`, o botão permanece desabilitado. Ao chegar em `success` ou `error`, ele volta
a ficar disponível.

## HistoryItem

Projeção de `Experiment` para a lista:

| Campo | Origem | Regra de exibição |
|---|---|---|
| `id` | `Experiment.id` | valor completo acessível |
| `created_at` | `Experiment.created_at` | data legível e valor original disponível |
| `prompt` | `Experiment.prompt` | resumo visual, texto completo no nome do controle |

Selecionar um item não altera nenhuma entidade; apenas carrega a visualização detalhada.
