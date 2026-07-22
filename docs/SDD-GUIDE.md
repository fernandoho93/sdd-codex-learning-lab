# Guia rápido de SDD

SDD significa *Spec-Driven Development*: antes de decidir como programar, registramos
o que precisa ser entregue e como saberemos que está correto.

## Artefatos

### Constituição

É o conjunto de regras permanentes do repositório. Uma feature não pode contrariá-la.
Neste projeto, ela exige especificação antes do código, testes, experimentos
reproduzíveis, proteção de dados e simplicidade.

### Especificação (`spec.md`)

Responde **o quê** e **por quê**. Contém histórias de usuário, cenários de aceite,
requisitos funcionais e resultados mensuráveis. Não deve escolher framework ou classe.

### Plano (`plan.md`)

Responde **como**. Aqui entram linguagem, dependências, armazenamento, estrutura de
pastas e decisões arquiteturais.

### Tarefas (`tasks.md`)

Transformam o plano em trabalho executável. Cada tarefa tem um identificador e, quando
pertence a uma história, uma marca como `[US1]`.

## Ciclo recomendado

```text
ideia -> especificar -> esclarecer -> planejar -> criar tarefas
      -> analisar -> implementar -> testar -> convergir
```

Uma mudança de comportamento começa na especificação. Uma mudança puramente técnica,
sem alterar o comportamento prometido, normalmente começa no plano ou nas tarefas.

## Como praticar

1. Escolha uma tarefa ainda não estudada em `tasks.md`.
2. Encontre o requisito ou história associado.
3. Leia o teste correspondente.
4. Faça uma pequena alteração deliberada e veja o teste falhar.
5. Reverta ou corrija a alteração e execute o teste novamente.
6. Registre o aprendizado em uma issue, commit ou anotação pessoal.

O objetivo não é produzir muitos documentos. É reduzir ambiguidades antes que elas
virem retrabalho no código.
