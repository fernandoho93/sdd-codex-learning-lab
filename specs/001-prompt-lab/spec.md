# Feature Specification: Laboratório Local de Prompts

**Feature Branch**: `001-prompt-lab`

**Created**: 2026-07-16

**Status**: Ready

**Input**: Criar uma primeira feature didática para estudar SDD e fundamentos de projetos de IA com segurança, sem depender inicialmente de serviços pagos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Executar um experimento local (Priority: P1)

Como estudante, quero enviar um prompt a um provedor simulado para observar uma resposta
reproduzível e entender o ciclo completo de um experimento.

**Why this priority**: É o menor fluxo que entrega valor e demonstra entrada, processamento,
saída, persistência e teste sem custo externo.

**Independent Test**: Executar um prompt em um diretório temporário e verificar que a resposta
é exibida e que exatamente um experimento completo é registrado.

**Acceptance Scenarios**:

1. **Given** um prompt com texto válido, **When** o estudante executa o experimento, **Then** uma resposta determinística é exibida e o experimento é salvo.
2. **Given** um prompt vazio ou somente com espaços, **When** o estudante tenta executar o experimento, **Then** uma mensagem clara é apresentada e nenhum experimento é salvo.

---

### User Story 2 - Consultar o histórico (Priority: P2)

Como estudante, quero listar experimentos anteriores para revisar o que testei e comparar
minhas entradas e resultados ao longo do estudo.

**Why this priority**: O histórico torna o laboratório útil entre sessões, mas depende do
registro produzido pelo fluxo principal.

**Independent Test**: Preparar dois registros locais, solicitar o histórico e verificar que
ambos aparecem do mais recente para o mais antigo com seus identificadores.

**Acceptance Scenarios**:

1. **Given** experimentos registrados, **When** o estudante consulta o histórico, **Then** os registros são mostrados do mais recente para o mais antigo.
2. **Given** nenhum experimento registrado, **When** o estudante consulta o histórico, **Then** uma mensagem de histórico vazio é apresentada sem criar arquivos desnecessários.

---

### User Story 3 - Inspecionar um experimento (Priority: P3)

Como estudante, quero abrir um experimento pelo identificador para analisar o prompt, a
resposta e os metadados usados para reproduzi-lo.

**Why this priority**: A inspeção detalhada aprofunda o aprendizado, mas o MVP já funciona sem ela.

**Independent Test**: Preparar um registro conhecido, consultá-lo pelo identificador e verificar
que todos os dados reproduzíveis são apresentados.

**Acceptance Scenarios**:

1. **Given** um identificador existente, **When** o estudante solicita seus detalhes, **Then** prompt, resposta, provedor, modelo, parâmetros, data e resultado são apresentados.
2. **Given** um identificador inexistente, **When** o estudante solicita seus detalhes, **Then** uma mensagem clara é apresentada sem alterar o histórico.

### Edge Cases

- Prompts vazios, somente com espaços ou maiores que 10.000 caracteres são rejeitados.
- Um arquivo de histórico ausente representa um histórico vazio.
- Uma linha de histórico inválida é ignorada com aviso, preservando os demais registros válidos.
- Falha ao gravar o histórico produz erro claro e não apresenta o experimento como salvo.
- Caracteres Unicode em prompts e respostas são preservados.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST aceitar um prompt textual entre 1 e 10.000 caracteres após remover espaços externos.
- **FR-002**: O sistema MUST gerar respostas determinísticas por meio de um provedor simulado que não realize chamadas de rede.
- **FR-003**: O sistema MUST exibir a resposta e indicar se o experimento foi salvo com sucesso.
- **FR-004**: O sistema MUST registrar cada experimento bem-sucedido com identificador único, prompt, resposta, provedor, modelo, parâmetros, data em UTC e estado final.
- **FR-005**: O sistema MUST armazenar os experimentos localmente em formato legível e manter os dados gerados fora do controle de versão.
- **FR-006**: O sistema MUST listar registros do mais recente para o mais antigo sem modificar o histórico.
- **FR-007**: O sistema MUST permitir consultar um registro completo por seu identificador.
- **FR-008**: O sistema MUST informar entradas inválidas, registros inexistentes, linhas corrompidas e falhas de armazenamento sem expor detalhes sensíveis.
- **FR-009**: Todos os fluxos funcionais MUST possuir testes automatizados que não acessem rede nem serviços pagos.

### Key Entities

- **Experiment**: Registro imutável de uma execução, contendo identificador, prompt, resposta, referência do provedor, referência do modelo, parâmetros, data em UTC e estado.
- **Provider Result**: Resposta produzida por um provedor, com texto, referência de modelo e metadados disponíveis.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um novo estudante consegue preparar o projeto e executar o primeiro experimento em até 15 minutos seguindo somente o quickstart.
- **SC-002**: 100% dos experimentos válidos exibidos como salvos podem ser recuperados pelo identificador após uma nova execução do programa.
- **SC-003**: Entradas inválidas e identificadores inexistentes recebem uma explicação útil em uma única tentativa, sem gravar ou alterar registros.
- **SC-004**: Um histórico com 1.000 experimentos locais é listado em até 2 segundos em um computador de desenvolvimento comum.
- **SC-005**: A suíte automatizada executa sem rede, sem chave de API e sem custo externo.

## Assumptions

- O primeiro usuário é um estudante executando o projeto localmente em um terminal.
- Há apenas um usuário e não é necessária autenticação nesta feature.
- Comparação de respostas, interface web e provedores reais ficam fora do escopo.
- O estudante é responsável por não inserir dados pessoais ou confidenciais.
- O armazenamento local será pequeno; 1.000 experimentos são suficientes para esta fase.

## AI and Data Boundaries

- Esta feature usa somente um provedor simulado, local e determinístico.
- Nenhum prompt, resposta, metadado ou segredo deixa a máquina.
- Dados pessoais, confidenciais e chaves de API são proibidos nos experimentos de estudo.
- A resposta simulada é conteúdo não confiável e não representa aconselhamento nem fato verificado.
- Latência, tokens e custo de provedores reais ficam fora do escopo; o custo desta feature é zero.
