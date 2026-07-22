# Local HTTP API Contract: PS5 Games Manager

Base path: `/api`. JSON UTF-8 é usado em todas as respostas, exceto `204 No Content`.

## Error envelope

```json
{
  "error": {
    "code": "validation_error",
    "message": "Revise os campos informados.",
    "fields": {"name": "O nome é obrigatório."}
  }
}
```

`fields` é omitido quando a falha não pertence a campos específicos.

## Game representation

```json
{
  "id": "18ae7218-f458-4df4-a5df-8a16b2a672a5",
  "name": "Astro Bot",
  "description": null,
  "genre": "Plataforma",
  "developer": "Team Asobi",
  "publisher": "Sony Interactive Entertainment",
  "release_date": "2024-09-06",
  "media_type": "physical",
  "status": "completed",
  "personal_rating": 9.5,
  "cover_url": "https://example.test/astro-bot.jpg",
  "notes": null,
  "source_name": "RAWG",
  "source_url": "https://rawg.io/games/astro-bot",
  "created_at": "2026-07-22T18:30:00Z",
  "updated_at": "2026-07-22T18:30:00Z"
}
```

Campos internos de normalização nunca são expostos. `source_name` e `source_url` formam um par
opcional estritamente validado; apenas a fonte `RAWG` e vínculos HTTPS sob `rawg.io` são aceitos.

## `POST /api/games`

Aceita os campos editáveis de `Game`. `id`, `created_at` e `updated_at` são rejeitados ou
ignorados conforme validação estrita definida na implementação.

- `201`: registro completo criado; cabeçalho `Location: /api/games/{id}`.
- `400 validation_error`: JSON inválido, tipo incorreto ou regra de campo violada.
- `409 duplicate_game`: já existe jogo com nome equivalente.
- `500 storage_error`: falha local sem detalhes internos.

## `GET /api/games`

Query opcional: `search`, `genre`, `status`. Critérios são combinados.

- `200`: `{"items": [<Game>], "filters": {"genres": ["..."]}}`.
- `400 validation_error`: status ou parâmetros inválidos/repetidos.
- `500 storage_error`: falha de leitura.

Itens são ordenados por nome e ID. Uma consulta sem correspondência retorna `items: []`.

## `GET /api/games/{id}`

- `200`: registro completo.
- `404 game_not_found`: identificador ausente ou inexistente.
- `500 storage_error`: falha de leitura.

## `PUT /api/games/{id}`

Substitui todos os campos editáveis. O frontend envia o estado completo do formulário.

- `200`: registro completo atualizado.
- `400 validation_error`: entrada inválida.
- `404 game_not_found`: registro inexistente.
- `409 duplicate_game`: nome conflita com outro registro.
- `500 storage_error`: falha local; registro anterior permanece íntegro.

## `DELETE /api/games/{id}`

A confirmação pertence à interface; a API executa a remoção solicitada.

- `204`: remoção concluída, corpo vazio.
- `404 game_not_found`: registro inexistente.
- `500 storage_error`: falha local.

## `GET /api/catalog/search?query={text}`

Consulta opcional detalhada em [rawg-adapter.md](rawg-adapter.md).

- `200`: candidatos externos e atribuição.
- `400 validation_error`: termo vazio ou maior que 200 caracteres.
- `503 catalog_not_configured`: chave ausente.
- `502 catalog_unavailable`: timeout, resposta inválida ou falha remota.
- `429 catalog_rate_limited`: cota do provedor excedida.

Nenhuma resposta inclui chave, URL autenticada completa ou conteúdo interno da exceção.

## Static routes

- `GET /`: HTML principal.
- `GET /assets/app.css`: estilos.
- `GET /assets/app.js`: comportamento.
- Rota desconhecida: erro JSON `404` para `/api/*` e resposta segura `404` para demais caminhos.
