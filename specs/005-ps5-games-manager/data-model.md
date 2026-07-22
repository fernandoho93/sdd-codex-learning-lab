# Data Model: PS5 Games Manager

## Game

Registro persistido e fonte de verdade da coleção local.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `id` | UUID string | yes | Gerado pelo sistema e imutável |
| `name` | string | yes | 1–200 caracteres após `strip()` |
| `name_key` | string | yes | `name.casefold()`, único e não exposto ao cliente |
| `description` | string or null | no | Até 2.000 caracteres |
| `genre` | string | yes | 1–100 caracteres |
| `genre_key` | string | yes | `genre.casefold()`, não exposto ao cliente |
| `developer` | string or null | no | Até 200 caracteres |
| `publisher` | string or null | no | Até 200 caracteres |
| `release_date` | ISO date or null | no | Data válida; futuro permitido |
| `media_type` | enum string | yes | `physical` ou `digital` |
| `status` | enum string | yes | `wishlist`, `purchased`, `playing`, `completed`, `abandoned` |
| `personal_rating` | decimal or null | no | 0 a 10, incremento de 0,5 |
| `cover_url` | string or null | no | HTTP/HTTPS, até 2.048 caracteres |
| `notes` | string or null | no | Até 5.000 caracteres |
| `source_name` | string or null | no | `RAWG` quando algum dado externo é mantido |
| `source_url` | URL string or null | no | Vínculo público de atribuição, nunca URL autenticada |
| `created_at` | UTC datetime string | yes | Gerado na criação e imutável |
| `updated_at` | UTC datetime string | yes | Igual a `created_at` na criação; muda em edição válida |

Valores opcionais vazios são normalizados para `null`. Espaços externos são removidos dos
textos; conteúdo interno e grafia de exibição são preservados. `source_name` e `source_url`
somente podem entrar por um candidato externo validado; não são campos editáveis livres.

## GameQuery

Objeto transitório para listagem.

| Field | Type | Default | Rules |
|---|---|---|---|
| `search` | string or null | null | Correspondência parcial em `name_key` |
| `genre` | string or null | null | Correspondência exata em `genre_key` |
| `status` | enum string or null | null | Um status permitido |

Todos os critérios fornecidos são combinados por interseção. A ordem padrão é nome crescente,
com `id` como desempate determinístico.

## ServiceError

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `code` | string | yes | Código estável, como `validation_error` |
| `message` | string | yes | Mensagem segura e compreensível |
| `fields` | object | no | Erros indexados por nome de campo |

Códigos mínimos: `validation_error`, `duplicate_game`, `game_not_found`, `storage_error`,
`catalog_not_configured`, `catalog_unavailable`, `catalog_rate_limited`.

## ExternalGameCandidate

Objeto transitório retornado pelo adaptador RAWG; nunca é persistido automaticamente.

| Field | Type | Required | Rules |
|---|---|---:|---|
| `external_id` | string | yes | Identificador opaco da fonte |
| `name` | string | yes | Título sugerido |
| `description` | string or null | no | Texto reduzido/limpo quando disponível |
| `genre` | string or null | no | Primeiro gênero sugerido |
| `developer` | string or null | no | Sugestão quando disponível |
| `publisher` | string or null | no | Sugestão quando disponível |
| `release_date` | ISO date or null | no | Sugestão quando válida |
| `cover_url` | HTTPS URL or null | no | Imagem sugerida |
| `source_name` | string | yes | `RAWG` |
| `source_url` | URL | yes | Vínculo de atribuição do resultado |

Selecionar um candidato copia valores e a atribuição ao formulário. O `Game` final é recriado
pelas regras locais, mantém apenas a proveniência necessária para crédito e não possui
sincronização automática com a fonte externa.

## Schema

```sql
CREATE TABLE schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE games (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    name_key TEXT NOT NULL UNIQUE,
    description TEXT,
    genre TEXT NOT NULL,
    genre_key TEXT NOT NULL,
    developer TEXT,
    publisher TEXT,
    release_date TEXT,
    media_type TEXT NOT NULL CHECK (media_type IN ('physical', 'digital')),
    status TEXT NOT NULL CHECK (status IN ('wishlist', 'purchased', 'playing', 'completed', 'abandoned')),
    personal_rating REAL CHECK (personal_rating IS NULL OR (personal_rating BETWEEN 0 AND 10 AND personal_rating * 2 = CAST(personal_rating * 2 AS INTEGER))),
    cover_url TEXT,
    notes TEXT,
    source_name TEXT,
    source_url TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

Índices adicionais cobrem `genre_key`, `status` e `name_key`. Migrações são aplicadas em ordem
numérica e registradas em `schema_migrations` dentro da mesma transação.

## State Transitions

O status pode mudar entre quaisquer valores permitidos; o sistema registra preferência e
progresso, não impõe uma sequência de jogo. Criação define os dois timestamps. Edição válida
preserva `id`/`created_at` e avança `updated_at`. Exclusão remove definitivamente o registro.
