# Modelo de Dados de Teste: Jornada de Livros no DemoQA

Esta feature não persiste dados. O modelo abaixo representa apenas informações observadas e usadas nas expectativas dos testes.

## BookExpectation

Representa o livro conhecido usado como oráculo legível.

| Campo | Tipo | Regra |
|---|---|---|
| `title` | string | Obrigatório e não vazio |
| `author` | string | Obrigatório e deve corresponder ao detalhe |
| `isbn` | string | Obrigatório, com 13 dígitos |

Exemplo desta feature: título `Git Pocket Guide`, autor `Richard E. Silverman`, ISBN `9781449325862`.

## SearchState

Representa os estados observáveis do catálogo durante a pesquisa.

| Estado | Entrada | Resultado esperado |
|---|---|---|
| Inicial | vazio | Ao menos um livro visível |
| Correspondente | título conhecido | Livro esperado visível e selecionável |
| Sem resultado | termo inexistente | Nenhuma linha de livro visível |
| Restaurado | campo limpo | Ao menos um livro novamente visível |

## TestEvidence

Representa artefatos locais gerados automaticamente quando um cenário falha.

| Campo | Regra |
|---|---|
| Cenário | Nome único e legível no relatório |
| Screenshot | Mantido somente em falha |
| Trace | Mantido na primeira falha |
| Relatório HTML | Separado do relatório da suíte local |

## Relações e transições

```text
Catálogo inicial -> pesquisa correspondente -> detalhe do BookExpectation -> catálogo
                 -> pesquisa inexistente -> lista vazia
                 -> campo limpo -> catálogo restaurado
```

Cada teste começa novamente no catálogo inicial; nenhuma transição de um teste é pré-condição de outro.
