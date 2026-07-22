# Especificação da Feature: API de Pokémon da PokéAPI

**Feature Branch**: `006-pokeapi-api`

**Created**: 2026-07-22

**Status**: Draft pausado — artefato reservado ao módulo 3

**Input**: User description: "Testar a API pública PokéAPI seguindo o padrão SDD, começando pela especificação com critérios de aceitação objetivos antes de gerar plano, tarefas e testes."

> **Nota de progressão do estudo**: esta especificação foi criada antes da descoberta exigida pelo guia. Ela permanece como rascunho não aprovado e não autoriza planejamento ou implementação. A fonte ativa no módulo 2 é [problem-brief.md](problem-brief.md); este documento deverá ser revisado a partir das decisões registradas ali quando o módulo 3 começar.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consultar Pokémon pelo nome (Priority: P1)

Como profissional de qualidade em aprendizado, quero consultar um Pokémon conhecido pelo nome para validar que o serviço fornece seus dados essenciais de forma pública e confiável.

**Why this priority**: É o menor fluxo que entrega valor e permite verificar disponibilidade, identificação do recurso e estrutura básica dos dados sem depender de outros cenários.

**Independent Test**: Consultar o Pokémon `pikachu` e confirmar sucesso, conteúdo estruturado e presença dos dados essenciais esperados para esse recurso.

**Acceptance Scenarios**:

1. **Given** que o serviço público está disponível, **When** o Pokémon `pikachu` é consultado pelo nome, **Then** a resposta indica sucesso e identifica o recurso com nome `pikachu` e ID `25`.
2. **Given** uma consulta bem-sucedida de `pikachu`, **When** seus dados básicos são inspecionados, **Then** altura e peso são números inteiros positivos e as coleções de tipos, habilidades e estatísticas não estão vazias.
3. **Given** uma consulta bem-sucedida de `pikachu`, **When** o formato da resposta é inspecionado, **Then** o conteúdo é estruturado como JSON válido.

---

### User Story 2 - Confirmar equivalência entre nome e ID (Priority: P2)

Como profissional de qualidade, quero consultar o mesmo Pokémon por nome e por ID para verificar que as duas formas de identificação representam o mesmo recurso.

**Why this priority**: A equivalência entre identificadores amplia a confiança no contrato de consulta sem introduzir um novo domínio de dados.

**Independent Test**: Consultar `pikachu` e `25` separadamente e comparar os campos que identificam o Pokémon e suas classificações principais.

**Acceptance Scenarios**:

1. **Given** que `pikachu` corresponde ao ID `25`, **When** o Pokémon é consultado pelas duas formas, **Then** ambas as respostas indicam sucesso e apresentam o mesmo ID e nome.
2. **Given** duas respostas referentes ao mesmo Pokémon, **When** seus tipos e habilidades são comparados, **Then** os nomes presentes nas duas respostas são equivalentes, independentemente da ordem em que sejam apresentados.

---

### User Story 3 - Listar Pokémon com paginação (Priority: P3)

Como profissional de qualidade, quero consultar uma página limitada da coleção de Pokémon para validar a navegação previsível por resultados sem carregar todo o catálogo.

**Why this priority**: A paginação é um comportamento distinto e relevante do serviço, mas não é necessária para comprovar a consulta individual do MVP.

**Independent Test**: Solicitar a primeira página com limite de cinco registros e deslocamento zero, confirmando metadados de navegação e o contrato básico de cada item listado.

**Acceptance Scenarios**:

1. **Given** o catálogo público de Pokémon, **When** a primeira página é solicitada com limite `5` e deslocamento `0`, **Then** a resposta indica sucesso e contém exatamente cinco resultados.
2. **Given** a primeira página limitada a cinco resultados, **When** seus metadados são inspecionados, **Then** a quantidade total é um número inteiro positivo, a referência para a página anterior é nula e existe uma referência para a próxima página.
3. **Given** uma página retornada com sucesso, **When** seus resultados são inspecionados, **Then** cada item possui nome não vazio e uma referência válida para seu detalhe.

---

### User Story 4 - Rejeitar Pokémon inexistente (Priority: P4)

Como profissional de qualidade, quero consultar um nome inexistente para confirmar que a ausência de um recurso é diferenciada de uma resposta válida.

**Why this priority**: O cenário negativo completa o contrato mínimo de consulta, mas não bloqueia o valor entregue pelos fluxos positivos.

**Independent Test**: Consultar um nome reservado para o teste que não corresponda a nenhum Pokémon e confirmar a indicação objetiva de recurso não encontrado.

**Acceptance Scenarios**:

1. **Given** um nome que não corresponde a nenhum Pokémon, **When** a consulta é realizada, **Then** a resposta indica recurso não encontrado com status `404`.
2. **Given** uma resposta de recurso não encontrado, **When** seu conteúdo é inspecionado, **Then** ela não é interpretada como um Pokémon válido nem precisa obedecer ao contrato de sucesso.

### Edge Cases

- O serviço externo pode estar indisponível, lento ou responder com falha transitória; isso deve ser distinguível de uma quebra do contrato funcional validado.
- O catálogo pode crescer ao longo do tempo; a quantidade total deve ser validada por tipo e limite mínimo, sem fixar um total exato.
- Campos opcionais ou novos podem aparecer nas respostas sem invalidar os campos essenciais definidos nesta especificação.
- Alterações legítimas nos dados de referência de `pikachu` exigem revisão da especificação antes de alterar as expectativas.
- Nomes vazios, diferenças de maiúsculas e minúsculas e identificadores fora do intervalo não pertencem a esta primeira fase.
- Testes de carga, varredura do catálogo completo e chamadas de alta frequência estão fora do escopo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A validação MUST consultar publicamente um Pokémon conhecido pelo nome e confirmar uma resposta de sucesso.
- **FR-002**: A resposta de sucesso MUST conter JSON válido e identificar `pikachu` pelo nome `pikachu` e pelo ID `25`.
- **FR-003**: O Pokémon validado MUST apresentar altura e peso como números inteiros positivos.
- **FR-004**: O Pokémon validado MUST apresentar ao menos um tipo, uma habilidade e uma estatística, cada qual com nome não vazio.
- **FR-005**: A validação MUST permitir consultar o Pokémon de referência tanto pelo nome quanto pelo ID.
- **FR-006**: As consultas por nome e por ID MUST retornar o mesmo ID, nome, conjunto de tipos e conjunto de habilidades para o Pokémon de referência.
- **FR-007**: A validação MUST consultar uma página da coleção com limite de cinco registros e deslocamento zero.
- **FR-008**: A página consultada MUST conter exatamente cinco resultados, quantidade total inteira positiva, ausência de página anterior e referência para a próxima página.
- **FR-009**: Cada resultado paginado MUST apresentar nome não vazio e referência válida para consulta de seu detalhe.
- **FR-010**: A consulta de um nome inexistente reservado para o cenário negativo MUST retornar status `404`.
- **FR-011**: Uma resposta de recurso inexistente MUST ser validada separadamente e MUST NOT ser obrigada a possuir o mesmo formato das respostas de sucesso.
- **FR-012**: Cada cenário MUST ser independente, somente leitura e executável sem credenciais.
- **FR-013**: A validação MUST limitar suas chamadas aos recursos necessários para os cenários definidos e MUST NOT realizar carga ou varredura completa do catálogo público.
- **FR-014**: A execução desta suíte externa MUST ocorrer somente quando solicitada explicitamente e permanecer separada das demais suítes do projeto.
- **FR-015**: Falhas MUST preservar informações suficientes sobre a solicitação, o status e o conteúdo recebido para permitir diagnóstico, sem registrar dados sensíveis.
- **FR-016**: As validações MUST aceitar campos adicionais e mudanças na quantidade total do catálogo, desde que os campos essenciais e os comportamentos definidos permaneçam válidos.

### Key Entities

- **Pokémon**: Recurso identificado por nome e ID, com dimensões e coleções de tipos, habilidades e estatísticas.
- **Tipo**: Classificação associada a um Pokémon, identificada por um nome não vazio.
- **Habilidade**: Capacidade associada a um Pokémon, identificada por um nome não vazio.
- **Estatística**: Medida associada a um Pokémon, identificada por um nome e um valor numérico.
- **Página de Pokémon**: Recorte da coleção contendo quantidade total, referências de navegação e uma lista limitada de recursos.
- **Referência de Pokémon**: Item resumido da coleção que contém nome e localização de seu detalhe.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um estudante consegue executar a validação principal de consulta por nome e compreender seu resultado em até cinco minutos seguindo a documentação da feature.
- **SC-002**: 100% das quatro histórias priorizadas podem ser executadas e avaliadas de forma independente.
- **SC-003**: 100% dos campos essenciais definidos para o Pokémon de referência são avaliados automaticamente quanto à presença, ao tipo e às regras de conteúdo aplicáveis.
- **SC-004**: As consultas por nome e ID apresentam 100% de equivalência nos identificadores, tipos e habilidades definidos nesta fase.
- **SC-005**: A página solicitada retorna exatamente cinco itens válidos e metadados suficientes para identificar a página anterior e a próxima.
- **SC-006**: A ausência de um Pokémon é diferenciada de uma consulta bem-sucedida em 100% das execuções nas quais o serviço externo responde normalmente.
- **SC-007**: Quando o serviço externo está disponível, cada cenário termina em até 30 segundos.
- **SC-008**: Uma execução completa realiza somente as chamadas necessárias aos quatro cenários e não percorre o catálogo inteiro.

## Assumptions

- O serviço público da PokéAPI v2 permanece disponível e acessível sem autenticação.
- O Pokémon `pikachu` permanece identificado pelo ID `25`, conforme o domínio estável da série.
- O catálogo contém mais de cinco Pokémon e oferece navegação após a primeira página.
- O nome reservado para o cenário negativo será suficientemente específico para não coincidir com um recurso real durante a vida desta feature.
- Esta fase cobre apenas consultas do domínio de Pokémon; espécies, evoluções, movimentos, itens, imagens e outros domínios ficam para features futuras.
- A resposta de recurso inexistente pode ter formato diferente das respostas de sucesso; o status é o contrato obrigatório desta fase.
- A disponibilidade e a latência da dependência externa estão fora do controle do projeto.
- As validações devem respeitar o uso justo do serviço público, mantendo baixo volume de chamadas e sem testes de carga.
