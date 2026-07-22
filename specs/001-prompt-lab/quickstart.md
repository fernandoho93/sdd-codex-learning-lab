# Quickstart: Laboratório Local de Prompts

## 1. Preparar

Na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## 2. Validar

```powershell
python -m unittest discover -s tests -v
```

Resultado esperado: todos os testes terminam com `OK` e nenhuma conexão de rede é feita.

## 3. Executar o cenário principal

```powershell
prompt-lab run "Explique SDD em três frases"
```

Resultado esperado: uma resposta começando por `Simulação local:` e um UUID de experimento.

## 4. Consultar o histórico

```powershell
prompt-lab history
```

O experimento anterior deve aparecer com identificador, data UTC e resumo do prompt.

## 5. Inspecionar

Copie o identificador exibido e execute:

```powershell
prompt-lab show SEU_IDENTIFICADOR
```

Confira os campos definidos em [data-model.md](data-model.md) e o comportamento documentado
em [contracts/cli.md](contracts/cli.md).

## Limpeza local

Os dados ficam em `data/experiments.jsonl`. Apagar esse arquivo reinicia apenas seu histórico
local; ele nunca deve ser versionado.
