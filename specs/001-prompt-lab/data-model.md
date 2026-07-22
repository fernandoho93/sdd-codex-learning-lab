# Data Model: Laboratório Local de Prompts

## Experiment

Registro imutável de uma execução concluída.

| Campo | Tipo | Regra |
|---|---|---|
| `id` | texto | UUID único e não vazio |
| `prompt` | texto | 1 a 10.000 caracteres após normalização externa |
| `response` | texto | não vazio |
| `provider` | texto | identificador não secreto do provedor |
| `model` | texto | identificador do modelo ou simulador |
| `parameters` | objeto | parâmetros reproduzíveis, sem segredos |
| `created_at` | texto | data/hora UTC no formato ISO 8601 |
| `status` | texto | `completed` nesta feature |

O registro não é atualizado depois de gravado. Uma nova execução cria outro identificador.

## ProviderResult

Valor retornado pelo limite de provedor antes da criação do experimento.

| Campo | Tipo | Regra |
|---|---|---|
| `text` | texto | resposta não vazia |
| `provider` | texto | `fake` nesta feature |
| `model` | texto | `deterministic-study-v1` nesta feature |
| `parameters` | objeto | vazio ou somente valores serializáveis |

## Relacionamentos e fluxo

```text
prompt válido -> ProviderResult -> Experiment -> arquivo JSONL
```

Uma linha inválida no arquivo não invalida as demais. O repositório retorna os registros válidos
e avisos separados para que a interface informe a degradação sem perder o histórico utilizável.
