# Feature Specification: Interface Web do Prompt Lab

**Feature Branch**: `002-web-prompt-lab`

**Created**: 2026-07-18

**Status**: Ready

**Input**: Disponibilizar o laboratório local de prompts em uma interface web e validar as jornadas principais com testes de navegador escritos em TypeScript.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Executar um prompt no navegador (Priority: P1)

Como estudante, quero escrever e executar um prompt em uma página web para observar a
resposta simulada e o identificador do experimento sem usar o terminal.

**Why this priority**: É a menor jornada web que entrega valor e permite aprender testes E2E
sobre um comportamento já protegido por testes de domínio.

**Independent Test**: Abrir a página, preencher um prompt válido, executar e verificar a
resposta simulada, a confirmação de persistência e o identificador do novo experimento.

**Acceptance Scenarios**:

1. **Given** a página do laboratório disponível, **When** o estudante informa um prompt válido e solicita a execução, **Then** a resposta simulada e o identificador salvo são exibidos.
2. **Given** um campo vazio ou somente com espaços, **When** o estudante solicita a execução, **Then** um erro claro é anunciado e nenhum resultado anterior é apresentado como novo.
3. **Given** um estudante usando somente teclado, **When** ele navega pelo formulário e executa um prompt, **Then** todos os controles e o resultado permanecem acessíveis e identificáveis.

---

### User Story 2 - Consultar o histórico na página (Priority: P2)

Como estudante, quero visualizar os experimentos anteriores para revisar rapidamente os
prompts executados durante a sessão de estudo.

**Why this priority**: Reaproveita o histórico já existente e amplia o valor da interface após
o fluxo principal estar funcional.

**Independent Test**: Criar um experimento pela página e verificar que ele aparece no histórico
com identificador, data e resumo do prompt, sem recarregar manualmente a página.

**Acceptance Scenarios**:

1. **Given** um experimento salvo, **When** sua execução termina, **Then** ele aparece no início do histórico.
2. **Given** nenhum experimento salvo, **When** a página carrega, **Then** o estado vazio é apresentado sem erro.
3. **Given** uma falha ao consultar o histórico, **When** a página recebe a falha, **Then** uma mensagem recuperável é mostrada sem impedir uma nova tentativa.

---

### User Story 3 - Inspecionar detalhes no navegador (Priority: P3)

Como estudante, quero selecionar um item do histórico para consultar os dados reproduzíveis
do experimento na própria página.

**Why this priority**: A inspeção completa é útil para análise, mas não bloqueia a execução nem
a listagem básica.

**Independent Test**: Selecionar um registro conhecido e verificar prompt, resposta, provedor,
modelo, data, estado e identificador em uma região de detalhes.

**Acceptance Scenarios**:

1. **Given** um item no histórico, **When** o estudante seleciona seus detalhes, **Then** todos os metadados reproduzíveis são exibidos.
2. **Given** um registro que deixou de existir, **When** o estudante tenta abri-lo, **Then** um erro claro é anunciado e a página continua utilizável.

### Edge Cases

- Prompts com Unicode, quebras de linha e exatamente 10.000 caracteres são aceitos.
- Prompts com mais de 10.000 caracteres são rejeitados sem criar experimento.
- Cliques repetidos durante uma execução não criam registros duplicados.
- Falhas de rede ou respostas inválidas não deixam o formulário permanentemente bloqueado.
- Textos longos não ultrapassam visualmente os limites da página.
- O estado de carregamento é perceptível sem depender apenas de cor.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A página MUST oferecer um campo de prompt claramente identificado e um controle de execução.
- **FR-002**: A página MUST aceitar os mesmos limites e regras de validação do laboratório existente.
- **FR-003**: Uma execução válida MUST exibir resposta, identificador e confirmação de persistência.
- **FR-004**: Durante uma execução, o controle MUST impedir envios duplicados e comunicar o estado de processamento.
- **FR-005**: Erros de entrada, comunicação, servidor e armazenamento MUST ser apresentados em linguagem clara e recuperável.
- **FR-006**: A página MUST carregar e apresentar o histórico do mais recente para o mais antigo.
- **FR-007**: Um experimento recém-criado MUST aparecer no histórico sem recarregamento manual da página.
- **FR-008**: A página MUST permitir consultar todos os dados reproduzíveis de um experimento selecionado.
- **FR-009**: Formulário, mensagens, histórico e detalhes MUST ser operáveis por teclado e possuir nomes acessíveis.
- **FR-010**: Os testes automatizados de navegador MUST usar o provedor simulado e dados isolados, sem rede externa, chave ou custo.

### Key Entities

- **Web Experiment View**: Representação exibida de um experimento existente, sem alterar seus dados de domínio.
- **Execution State**: Estado transitório da interface: ocioso, processando, concluído ou com erro.
- **History Item**: Resumo selecionável contendo identificador, data e trecho do prompt.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um estudante conclui sua primeira execução pela página em até 2 minutos sem consultar instruções do terminal.
- **SC-002**: 100% das execuções confirmadas como salvas aparecem no histórico e podem ser inspecionadas na mesma sessão.
- **SC-003**: Entradas inválidas recebem uma mensagem útil em até 1 segundo e não criam registros.
- **SC-004**: As jornadas de executar, listar e inspecionar passam automaticamente em um navegador suportado sem acessar serviços externos.
- **SC-005**: Todos os controles e resultados essenciais podem ser alcançados e compreendidos usando somente teclado e nomes acessíveis.

## Assumptions

- A interface atende um único estudante local e não requer autenticação.
- O servidor e o navegador executam na mesma máquina durante esta fase.
- O domínio, o provedor simulado e o arquivo de histórico existentes serão reutilizados.
- Layout móvel avançado, autenticação, múltiplos usuários e provedor real permanecem fora do escopo.
- O navegador possui suporte atual a JavaScript e recursos básicos de acessibilidade web.

## AI and Data Boundaries

- A interface utiliza exclusivamente o provedor simulado local desta fase.
- Nenhum prompt, resposta, metadado ou segredo é enviado para fora da máquina.
- Conteúdo gerado continua sendo tratado como não confiável.
- Dados de teste e relatórios de navegador permanecem em diretórios locais ignorados pelo Git.
- Latência, tokens e custos de modelos reais continuam fora do escopo e serão tratados em feature própria.
