# Especificação da Feature: Jornada de Livros no DemoQA

**Feature Branch**: `003-demoqa-books-e2e`

**Created**: 2026-07-19

**Status**: Ready

**Input**: Criar uma base de estudo para testes automatizados de ponta a ponta na página pública de livros do DemoQA, começando por jornadas simples e evoluindo de forma incremental.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consultar o catálogo de livros (Priority: P1)

Como profissional de qualidade em aprendizado, quero abrir a livraria e reconhecer seus elementos essenciais para validar que o catálogo está disponível antes de testar interações mais complexas.

**Why this priority**: É a menor verificação que produz valor, estabelece a base da automação e ajuda a aprender navegação, localização e asserções.

**Independent Test**: Abrir a página pública de livros e confirmar que a estrutura do catálogo, a pesquisa e ao menos um livro identificável estão disponíveis.

**Acceptance Scenarios**:

1. **Given** que o serviço público está disponível, **When** o visitante abre o catálogo, **Then** identifica a página pelo endereço e pelas colunas, encontra o campo de pesquisa e ao menos um livro com título.
2. **Given** que o catálogo foi carregado, **When** o visitante não realiza nenhuma pesquisa, **Then** os livros permanecem disponíveis para consulta.

---

### User Story 2 - Pesquisar um livro (Priority: P2)

Como visitante, quero pesquisar um título conhecido para encontrar rapidamente o livro desejado no catálogo.

**Why this priority**: A pesquisa é a principal interação pública da página e introduz preenchimento de campos, filtragem e estados com e sem resultado.

**Independent Test**: Informar um título existente, confirmar que o resultado correspondente permanece visível e depois pesquisar um termo inexistente para confirmar o estado vazio.

**Acceptance Scenarios**:

1. **Given** o catálogo aberto, **When** o visitante pesquisa pelo título completo de um livro existente, **Then** somente resultados compatíveis são apresentados e o título procurado pode ser selecionado.
2. **Given** o catálogo aberto, **When** o visitante pesquisa um termo que não corresponde a nenhum livro, **Then** nenhum livro é apresentado como resultado.
3. **Given** uma pesquisa aplicada, **When** o visitante limpa o campo, **Then** o catálogo volta a apresentar livros.

---

### User Story 3 - Consultar detalhes de um livro (Priority: P3)

Como visitante, quero abrir um resultado para confirmar os dados essenciais do livro e retornar ao catálogo.

**Why this priority**: Completa uma jornada de navegação entre páginas, mas depende de o catálogo e a seleção de um livro já estarem compreendidos.

**Independent Test**: Selecionar um título conhecido, validar título, autor e identificador do livro e retornar à página do catálogo.

**Acceptance Scenarios**:

1. **Given** um livro visível no catálogo, **When** o visitante seleciona seu título, **Then** a página de detalhes apresenta o mesmo título, seu autor e seu ISBN.
2. **Given** a página de detalhes aberta, **When** o visitante solicita o retorno à livraria, **Then** o catálogo volta a ser apresentado.

### Edge Cases

- Um termo sem correspondência deve produzir uma lista vazia, sem exibir livros incorretos.
- Ao limpar uma pesquisa, o catálogo deve voltar a apresentar resultados sem exigir recarregamento manual.
- Conteúdo publicitário e recursos de terceiros não fazem parte da jornada e não devem determinar o resultado dos testes.
- Indisponibilidade, lentidão ou alteração de dados do serviço público deve ser distinguida de uma regressão no código de testes.
- O teste não deve criar conta, autenticar usuário nem alterar o perfil público de demonstração.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A validação MUST confirmar que a página pública do catálogo pode ser aberta e identificada.
- **FR-002**: A validação MUST confirmar a disponibilidade do campo de pesquisa e de ao menos um livro identificável.
- **FR-003**: A pesquisa por um título existente MUST manter um resultado correspondente visível e selecionável.
- **FR-004**: A pesquisa por um termo inexistente MUST resultar em nenhum livro apresentado.
- **FR-005**: A remoção do termo pesquisado MUST restaurar a apresentação de livros.
- **FR-006**: A seleção de um livro conhecido MUST apresentar detalhes coerentes de título, autor e ISBN.
- **FR-007**: A página de detalhes MUST permitir o retorno ao catálogo.
- **FR-008**: Cada cenário automatizado MUST iniciar em estado independente e não MUST depender da ordem de execução dos demais.
- **FR-009**: Falhas MUST preservar evidências suficientes para diferenciar defeito da aplicação, indisponibilidade externa e problema de automação.
- **FR-010**: A suíte MUST permanecer separada dos testes locais do Prompt Lab e somente acessar o serviço externo quando explicitamente solicitada.

### Key Entities

- **Catálogo**: Conjunto público de livros que pode ser visualizado e filtrado.
- **Livro**: Item do catálogo identificado por título, autor e ISBN, com uma página de detalhes.
- **Consulta**: Texto informado pelo visitante para filtrar os livros apresentados.
- **Evidência de teste**: Resultado, captura ou rastreamento usado para investigar uma falha.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um estudante consegue executar a primeira validação do catálogo em até 5 minutos seguindo o quickstart.
- **SC-002**: 100% das três jornadas priorizadas podem ser executadas e avaliadas de forma independente.
- **SC-003**: Os cenários positivos e o estado sem resultados produzem conclusões objetivas, sem inspeção visual manual obrigatória.
- **SC-004**: Toda falha gera ao menos uma evidência de diagnóstico e identifica claramente o cenário afetado.
- **SC-005**: A suíte externa e a suíte local podem ser executadas separadamente, sem iniciar serviços ou cenários desnecessários.

## Assumptions

- A página `https://demoqa.com/books` é um catálogo demonstrativo público e não oferece uma jornada real de compra, carrinho ou pagamento.
- O primeiro incremento usa um navegador de desktop e não cobre responsividade ou compatibilidade entre múltiplos navegadores.
- O catálogo contém o livro público conhecido “Git Pocket Guide”; mudanças nos dados do DemoQA podem exigir manutenção do dado de teste.
- O ambiente de execução possui acesso à internet e o serviço DemoQA pode apresentar publicidade, lentidão ou indisponibilidade fora do controle do projeto.
- Login, cadastro, perfil, inclusão e exclusão de livros permanecem fora do escopo desta feature para evitar mutações em serviço público.
- A evolução para cenários autenticados será especificada em uma feature posterior, com estratégia própria para dados e credenciais.
