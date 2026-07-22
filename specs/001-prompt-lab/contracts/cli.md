# CLI Contract: `prompt-lab`

## Convenções

- Saída normal usa `stdout`.
- Mensagens de erro e avisos usam `stderr`.
- Código `0` representa sucesso; código `2`, entrada ou comando inválido; código `1`, falha operacional.
- O caminho de dados padrão é `data/experiments.jsonl` e pode ser substituído por
  `PROMPT_LAB_DATA_FILE`, facilitando testes e isolamento.

## `prompt-lab run <prompt>`

Executa o prompt no provedor simulado, mostra a resposta e o identificador salvo.

Exemplo de saída:

```text
Resposta: Simulação local: ...
Experimento salvo: <uuid>
```

Prompt vazio ou maior que 10.000 caracteres retorna código `2` e não grava registro.

## `prompt-lab history`

Lista do mais recente para o mais antigo:

```text
<uuid> | <data UTC> | <resumo do prompt>
```

Sem registros, mostra `Nenhum experimento registrado.` e retorna código `0`.

## `prompt-lab show <id>`

Mostra todos os campos reproduzíveis do experimento em formato legível. Um identificador
inexistente retorna código `2` e mensagem clara.
