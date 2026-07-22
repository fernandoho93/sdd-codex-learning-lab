# Modelo de Dados de Teste: API de Livros do DemoQA

Os modelos representam respostas externas observadas; nada é persistido pelo projeto.

## Book

| Campo | Tipo esperado | Regra desta fase |
|---|---|---|
| `isbn` | string | 13 dígitos e não vazio |
| `title` | string | não vazio |
| `subTitle` | string | presente |
| `author` | string | não vazio |
| `publish_date` | string | presente |
| `publisher` | string | não vazio |
| `pages` | number | inteiro positivo |
| `description` | string | presente |
| `website` | string | presente |

## BookCollection

| Campo | Tipo esperado | Regra |
|---|---|---|
| `books` | array de `Book` | coleção não vazia |

## ApiError

| Campo | Tipo esperado | Regra negativa |
|---|---|---|
| `code` | string | `1205` para ISBN inexistente |
| `message` | string | não vazia e informa indisponibilidade |

## ReferenceBook

```text
isbn:   9781449325862
title:  Git Pocket Guide
author: Richard E. Silverman
```

## Relações

```text
BookCollection.books[*] --isbn--> Book detalhado
ISBN inexistente ----------------> ApiError
```

O cenário de detalhe obtém catálogo e detalhe dentro do mesmo teste e compara os campos essenciais, mantendo independência entre cenários.
