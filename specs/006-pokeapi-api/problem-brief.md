# Síntese do problema: aprendizado de SDD com a PokéAPI

**Data**: 2026-07-22  
**Módulo**: 2 — Descoberta e enquadramento do problema  
**Status**: Em revisão pelo estudante

## Demanda em uma frase

Como estudante de qualidade de software, quero usar uma mudança pequena e segura envolvendo a PokéAPI para aprender a transformar uma demanda vaga em um problema delimitado antes de especificar ou implementar uma solução.

## Problema

O estudante precisa praticar SDD de forma acumulativa no mesmo repositório, mas a intenção inicial — “testar a PokéAPI” — ainda não esclarece qual aprendizado deve ser demonstrado, quais comportamentos importam, quais evidências serão aceitas e onde termina o exercício. Sem esse enquadramento, há risco de começar diretamente por ferramentas e testes, produzir cobertura excessiva e perder a evidência pedagógica esperada no módulo 2.

## Resultado esperado

Ao concluir a descoberta, o estudante consegue explicar, sem antecipar a implementação:

- quem se beneficia da mudança;
- qual problema de aprendizado está sendo resolvido;
- quais eventos e resultados precisam ser observados;
- quais restrições e dependências existem;
- o que pertence e o que não pertence ao primeiro recorte;
- quais afirmações ainda são hipóteses ou perguntas abertas.

## Evidências disponíveis

- O repositório é próprio, local e destinado a estudo, reduzindo o risco operacional.
- O projeto já contém exemplos de validação de serviços externos, mostrando que o domínio de testes pode ser praticado no mesmo repositório.
- A PokéAPI oferece dados públicos de consulta e não exige credenciais para o uso proposto.
- A demanda atual escolhe Codex como ferramenta e limita os ajustes ao conteúdo estudado até o módulo 2.
- Uma especificação detalhada foi criada antes desta descoberta; ela é evidência de avanço prematuro e ficará pausada até o módulo correspondente.
- O estado atual do Git ainda não fornece uma linha de base limpa e versionada para reverter toda a experiência com segurança.

## Mapa de atores e eventos

| Ator | Evento | Necessidade | Resultado observável |
|------|--------|------------|----------------------|
| Estudante de qualidade | Inicia o módulo 2 com a intenção vaga de testar um serviço público | Delimitar o problema antes de escolher a solução | Consegue apresentar problema, resultado, escopo e dúvidas em linguagem simples |
| Estudante de qualidade | Analisa exemplos de dados disponíveis | Separar fatos, exemplos e hipóteses | Registra exemplos representativos sem convertê-los prematuramente em casos de teste |
| Estudante de qualidade | Encontra uma informação desconhecida | Evitar que uma suposição seja tratada como requisito | Mantém a questão aberta ou a identifica explicitamente como hipótese |
| Serviço público externo | Responde normalmente a uma consulta futura | Fornecer um domínio real e de baixo risco para o estudo | A informação recebida pode ser distinguida de ausência de recurso |
| Serviço público externo | Fica lento ou indisponível | Não confundir dependência externa com regra do domínio | A indisponibilidade permanece registrada como restrição do ambiente |
| Codex | Explora o repositório e organiza a descoberta | Apoiar o enquadramento sem decidir silenciosamente pelo estudante | Decisões, dúvidas e limites ficam visíveis para revisão humana |

## Regras e exemplos de descoberta

### Regras conhecidas

- O estudo deve continuar no mesmo repositório e usar somente Codex.
- A mudança deve ser pequena, reversível e sem dados sensíveis ou credenciais de produção.
- O domínio inicial deve permanecer somente leitura e com baixo volume de acesso.
- Até o encerramento do módulo 2, o foco é o problema; especificação final, plano, tarefas e testes ainda não são entregas autorizadas.
- Informações desconhecidas não devem ser preenchidas como fatos: devem aparecer como hipótese ou pergunta aberta.

### Exemplos que ajudam a compreender o domínio

- Um Pokémon conhecido representa um recurso que se espera encontrar.
- Um nome inventado representa a ausência de um recurso.
- Uma pequena parte do catálogo representa a necessidade de navegar por uma coleção sem percorrê-la por inteiro.
- Uma falha temporária do serviço representa uma restrição externa, não necessariamente um defeito na regra estudada.

Esses exemplos ajudam a conversar sobre o problema. Eles ainda não constituem critérios de aceitação nem casos de teste.

## Hipóteses

- **H-001**: O principal ator é o próprio estudante, e não um usuário final de um produto de Pokémon.
- **H-002**: O resultado educacional mais importante é demonstrar o ciclo SDD, e não obter cobertura ampla da PokéAPI.
- **H-003**: Um domínio público, somente leitura e sem autenticação é suficientemente seguro para a mudança de estudo.
- **H-004**: Um Pokémon conhecido, um inexistente e uma coleção pequena fornecem exemplos suficientes para descobrir o primeiro recorte.
- **H-005**: A especificação já criada pode ser reaproveitada no módulo 3 depois de ser confrontada com as decisões desta descoberta.

## Perguntas abertas

### Usuários e valor

1. O único público desta feature é o estudante ou o material também deverá orientar outros iniciantes?
2. O aprendizado principal deve enfatizar o raciocínio SDD, os fundamentos de serviços HTTP ou ambos com o mesmo peso?
3. Que explicação ou demonstração fará o estudante considerar que compreendeu o problema?

### Eventos e comportamentos relevantes

4. Quais situações do domínio são indispensáveis para o primeiro incremento: encontrar um recurso, não encontrá-lo e navegar por uma coleção?
5. A equivalência entre duas formas de identificar o mesmo recurso é parte do problema inicial ou um refinamento posterior?
6. Como o estudo deve diferenciar uma falha do serviço externo de um comportamento incorreto do recurso consultado?

### Restrições e riscos

7. Qual quantidade máxima de chamadas externas por execução é considerada adequada ao uso responsável?
8. A execução precisa funcionar em ambientes sem acesso à internet ou essa limitação será apenas documentada?
9. Existe alguma restrição adicional sobre imagens, nomes ou outros dados fornecidos pelo serviço?

### Evidências e resultado esperado

10. Quais evidências serão exigidas posteriormente: saída legível, relatório, anexos de resposta ou combinação desses itens?
11. O estudante deverá explicar cada resultado manualmente ou bastará que a evidência seja reproduzível?
12. Quais medidas demonstrarão aprendizado sem transformar a descoberta em uma especificação técnica?

### Continuidade do estudo

13. A especificação antecipada deve ser revisada no módulo 3 ou reescrita a partir desta síntese?
14. Qual será a linha de base Git aceita antes de realizar novos exercícios que exijam reversão e commit?

## Escopo do módulo 2

- Enquadrar a demanda de aprendizado relacionada à PokéAPI.
- Identificar atores, eventos, resultados, evidências e restrições.
- Separar regras conhecidas, exemplos, hipóteses e perguntas abertas.
- Definir o primeiro limite de escopo sem escolher ferramentas ou arquitetura.
- Registrar o aprendizado e as pendências para revisão do estudante.

## Fora do escopo

- Aprovar ou completar a especificação funcional.
- Definir arquitetura, linguagem, biblioteca, estrutura de arquivos de implementação ou estratégia detalhada de testes.
- Criar plano, tarefas, código ou testes automatizados.
- Cobrir todos os domínios ou recursos oferecidos pela PokéAPI.
- Executar testes de carga, segurança ofensiva ou varredura completa do catálogo.
- Resolver indisponibilidade ou mudanças do serviço externo.

## Custo do não atendimento

- Avançar para a solução sem compreender o objetivo educacional.
- Criar testes frágeis ou numerosos que não demonstram o aprendizado pretendido.
- Confundir restrições do serviço externo com regras do problema.
- Aumentar retrabalho em especificação, planejamento e implementação.
- Perder a rastreabilidade entre a demanda original, as decisões e as evidências produzidas.

## Critérios de sucesso observáveis

- O estudante consegue explicar o problema, o ator principal e o resultado esperado em até dois minutos, sem citar uma ferramenta de implementação.
- O documento contém ao menos um ator principal, cinco eventos relevantes e os resultados observáveis associados.
- O documento mantém visíveis pelo menos dez perguntas abertas e três hipóteses.
- Escopo e fora do escopo podem ser identificados sem interpretação adicional.
- Cada afirmação relevante está apresentada como evidência, regra conhecida, exemplo, hipótese ou pergunta, evitando decisões implícitas.
- O estudante revisa esta síntese e registra quais hipóteses foram confirmadas, rejeitadas ou mantidas antes de iniciar o módulo 3.

## Critério de passagem para o próximo módulo

- [x] O problema está descrito sem antecipar tecnologia de implementação.
- [x] Os atores e resultados esperados estão explícitos.
- [x] As hipóteses e perguntas sem resposta estão visíveis.
- [x] O fora do escopo está registrado.
- [ ] O estudante revisou a síntese e registrou suas respostas ou concordância.
- [ ] A linha de base do Git está adequada para versionar os artefatos e permitir reversão.

