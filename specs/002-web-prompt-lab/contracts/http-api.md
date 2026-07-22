# HTTP API Contract

Todas as respostas usam UTF-8 e JSON, exceto arquivos estáticos. Erros seguem:

```json
{"error": "mensagem clara"}
```

## `POST /api/experiments`

Corpo:

```json
{"prompt": "Explique SDD"}
```

- `201`: retorna o objeto completo do experimento salvo.
- `400`: JSON inválido, campo ausente, tipo incorreto ou prompt fora dos limites.
- `500`: falha de armazenamento ou erro operacional interno.

## `GET /api/experiments`

- `200`: `{"items": [<Experiment>], "warnings": ["..."]}` em ordem decrescente.
- `500`: falha operacional de leitura.

## `GET /api/experiments/{id}`

- `200`: objeto completo do experimento.
- `404`: identificador inexistente.
- `500`: falha operacional de leitura.

## Arquivos estáticos

- `GET /`: documento HTML principal.
- `GET /assets/app.css`: estilos.
- `GET /assets/app.js`: comportamento da página.
- Caminho desconhecido: `404`.
