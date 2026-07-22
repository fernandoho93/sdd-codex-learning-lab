# RAWG Adapter Contract

## Configuration

- `RAWG_API_KEY`: chave opcional lida somente pelo backend.
- `RAWG_API_BASE_URL`: padrão `https://api.rawg.io/api`; substituível em validação controlada.
- Timeout total: 5 segundos.
- Máximo: 10 resultados por consulta.

## Upstream request

O adaptador consulta o catálogo de jogos com o termo fornecido, chave, limite de resultados e
filtro da plataforma PlayStation 5. A URL autenticada nunca é registrada ou retornada.

## Local response

```json
{
  "items": [
    {
      "external_id": "3498",
      "name": "Grand Theft Auto V",
      "description": null,
      "genre": "Action",
      "developer": null,
      "publisher": null,
      "release_date": "2022-03-15",
      "cover_url": "https://media.rawg.io/media/games/example.jpg",
      "source_name": "RAWG",
      "source_url": "https://rawg.io/games/grand-theft-auto-v"
    }
  ],
  "attribution": {
    "text": "Dados e imagens fornecidos por RAWG",
    "url": "https://rawg.io/"
  }
}
```

Campos ausentes ou inválidos no provedor tornam-se `null`. HTML externo é removido e nenhum
valor é considerado confiável. Resultados sem nome, identificador, vínculo de fonte ou
compatibilidade com PS5 são descartados.

## Failure mapping

| Upstream condition | Local code | Behavior |
|---|---|---|
| chave ausente | `catalog_not_configured` | não realiza chamada |
| HTTP 429 | `catalog_rate_limited` | permite tentar depois |
| timeout, DNS, TLS ou HTTP 5xx | `catalog_unavailable` | cadastro manual permanece disponível |
| JSON inválido ou forma inesperada | `catalog_unavailable` | não retorna dados parciais inseguros |
| HTTP 4xx diferente de 429 | `catalog_unavailable` | não expõe corpo ou chave |

## Test boundary

O cliente recebe uma função de transporte injetável. Testes fornecem respostas locais
determinísticas e verificam parâmetros já separados, sem rede e sem credenciais reais.

