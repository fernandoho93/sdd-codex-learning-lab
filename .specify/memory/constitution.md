<!--
Relatório de Impacto da Sincronização
- Alteração de versão: 1.0.0 -> 1.0.1
- Motivo da versão: tradução integral para PT-BR sem mudança de obrigações (PATCH)
- Princípios traduzidos para PT-BR:
  - Especificação Primeiro
  - Incrementos Pequenos e Independentes
  - Testes e Reprodutibilidade
  - IA Segura e Observável
  - Simplicidade e Aprendizado
- Seções traduzidas para PT-BR:
  - Restrições Técnicas e de Dados
  - Fluxo de Desenvolvimento
  - Governança
- Seções adicionadas: nenhuma
- Seções removidas: nenhuma
- Templates verificados, sem atualização necessária:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Skills do agente verificadas: ✅ .agents/skills/speckit-*/SKILL.md
- Documentação de execução verificada: ✅ README.md, docs/SDD-GUIDE.md e quickstart ativo
- Pendências: nenhuma
-->
# Constituição do Prompt Lab SDD

## Princípios Fundamentais

### I. Especificação Primeiro

Toda mudança de comportamento DEVE começar com uma especificação de feature testável. A
especificação DEVE descrever o valor para o usuário, os cenários de aceite, os casos de borda,
os requisitos funcionais e os critérios de sucesso mensuráveis antes do início da implementação.
As escolhas técnicas pertencem ao plano, não à especificação. Isso mantém as decisões
rastreáveis e impede que o código defina silenciosamente o produto.

### II. Incrementos Pequenos e Independentes

As features DEVEM ser divididas em histórias de usuário priorizadas que possam ser demonstradas
e testadas de forma independente. A menor história que entregue valor é o MVP preferencial.
Novas abstrações, serviços, interfaces ou dependências DEVEM resolver um requisito da
especificação ativa; infraestrutura especulativa é proibida. Isso torna o projeto acessível
para o aprendizado e limita o custo dos erros.

### III. Testes e Reprodutibilidade

Todo requisito funcional DEVE ser coberto por um teste automatizado ou por uma validação manual
explicitamente documentada quando a automação não for viável. Os testes DEVEM ser determinísticos
e NÃO DEVEM depender de chamadas pagas ou remotas a modelos. Experimentos de IA DEVEM registrar
metadados não secretos suficientes para reproduzir a configuração, incluindo prompt,
identificador do provedor, identificador do modelo quando aplicável, parâmetros, data e hora e
resultado. Uma feature não está concluída enquanto seus testes obrigatórios estiverem falhando.

### IV. IA Segura e Observável

Segredos, dados pessoais, conteúdo confidencial e dados gerados por experimentos NÃO DEVEM ser
versionados. Chamadas externas de IA DEVEM estar isoladas por uma fronteira de provedor, usar
timeouts explícitos e apresentar falhas sem perder dados locais. A saída de modelos DEVE ser
tratada como conteúdo não confiável. Features com provedores reais DEVEM expor latência, uso de
tokens quando disponível e custo estimado, ou declarar claramente quando uma métrica não estiver
disponível.

### V. Simplicidade e Aprendizado

A solução padrão DEVE favorecer a biblioteca padrão, uma interface de linha de comando,
armazenamento local e módulos claros até que os requisitos justifiquem maior complexidade. Cada
feature DEVE incluir um quickstart executável e explicar decisões importantes em linguagem
simples. Refatorações são permitidas somente quando os testes preservam o comportamento. A
clareza educacional é uma entrega do projeto, não um efeito colateral.

## Restrições Técnicas e de Dados

- Python 3.11 ou superior é a base para a primeira fase do projeto.
- Armazenamento local e legível por pessoas é preferível até que requisitos de escala
  justifiquem um banco de dados.
- Dependências de runtime DEVEM ser mínimas, documentadas e fixadas quando introduzidas.
- A configuração DEVE vir de argumentos ou variáveis de ambiente; segredos NUNCA DEVEM possuir
  valores padrão versionados.
- Dados gerados DEVEM permanecer em um diretório local ignorado pelo Git, salvo quando uma
  especificação definir explicitamente uma feature de exportação.

## Fluxo de Desenvolvimento

O trabalho DEVE seguir esta sequência: especificar, esclarecer quando necessário, planejar,
gerar tarefas, analisar, implementar, testar e convergir. As verificações da constituição são
obrigatórias antes e depois do design. As tarefas DEVEM referenciar arquivos concretos e mapear
o trabalho de implementação para uma história de usuário ou uma fundação compartilhada. Os
commits DEVERIAM ser pequenos e descrever uma única mudança lógica. Antes que uma feature seja
considerada concluída, seu quickstart e toda a suíte automatizada de testes DEVEM executar com
sucesso.

## Governança

Esta constituição prevalece sobre hábitos locais e preferências de uma feature. Alterações
exigem justificativa documentada, mudança de versão semântica, revisão de impacto nos templates
e nas features ativas e registro da data da alteração. Versões MAJOR removem ou redefinem um
princípio de modo incompatível; versões MINOR adicionam ou ampliam materialmente as regras;
versões PATCH esclarecem o texto sem modificar obrigações. Todo plano e toda revisão DEVEM
verificar a conformidade. Qualquer exceção justificada DEVE ser registrada na seção de controle
de complexidade do plano antes da implementação.

**Versão**: 1.0.1 | **Ratificada em**: 2026-07-16 | **Última alteração**: 2026-07-19
