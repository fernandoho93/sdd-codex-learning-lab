# Contrato HTTP Observado: DemoQA Book Store API

**Base URL**: `https://demoqa.com`

Contrato observado em 2026-07-19 a partir da página Swagger pública e de consultas somente leitura.

## GET `/BookStore/v1/Books`

### Requisição

- Autenticação: não exigida.
- Corpo: ausente.
- Cabeçalho recomendado: `Accept: application/json`.

### Resposta de sucesso

- Status: `200 OK`.
- `Content-Type`: contém `application/json`.
- Corpo:

```json
{
  "books": [
    {
      "isbn": "9781449325862",
      "title": "Git Pocket Guide",
      "subTitle": "A Working Introduction",
      "author": "Richard E. Silverman",
      "publish_date": "2020-06-04T08:48:39.000Z",
      "publisher": "O'Reilly Media",
      "pages": 234,
      "description": "...",
      "website": "http://..."
    }
  ]
}
```

## GET `/BookStore/v1/Book?ISBN={isbn}`

### Parâmetro

- `ISBN`: string enviada na query.

### ISBN existente `9781449325862`

- Status: `200 OK`.
- `Content-Type`: contém `application/json`.
- Corpo: um objeto `Book` cujo ISBN, título e autor correspondem ao catálogo.

### ISBN inexistente `0000000000000`

- Status: `400 Bad Request`.
- `Content-Type`: contém `application/json`.
- Corpo observado:

```json
{
  "code": "1205",
  "message": "ISBN supplied is not available in Books Collection!"
}
```

## Fora do contrato desta feature

- Ausência ou formato inválido do parâmetro ISBN.
- Criação de usuário e geração de token.
- Inclusão, substituição ou remoção de livros do perfil.
- Garantia de disponibilidade, desempenho ou imutabilidade dos dados do serviço externo.
