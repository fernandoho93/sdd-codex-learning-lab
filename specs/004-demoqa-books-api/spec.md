# Especificação da Feature: API de Livros do DemoQA

**Feature Branch**: `004-demoqa-books-api`

**Created**: 2026-07-19

**Status**: Ready

**Input**: Criar uma estrutura inicial de testes automatizados da API pública de livros do DemoQA, integrada ao projeto de estudo e seguindo o fluxo SDD existente.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consultar o catálogo pela API (Priority: P1)

Como profissional de qualidade em aprendizado, quero consultar o catálogo pela interface de serviço para validar o contrato básico sem depender da renderização da página.

**Why this priority**: É a menor validação de API que entrega valor e ensina requisição, status, cabeçalhos, estrutura e conteúdo da resposta.

**Independent Test**: Realizar uma consulta pública ao catálogo e confirmar sucesso, conteúdo JSON, coleção não vazia e presença de um livro conhecido com campos essenciais.

**Acceptance Scenarios**:

1. **Given** que o serviço público está disponível, **When** o catálogo é consultado, **Then** a resposta indica sucesso e contém uma coleção de livros.
2. **Given** uma resposta de catálogo bem-sucedida, **When** seus livros são inspecionados, **Then** cada item observado possui ISBN, título, autor, editora e quantidade de páginas em formatos válidos.
3. **Given** o catálogo atual do ambiente demonstrativo, **When** a coleção é consultada, **Then** o livro de referência “Git Pocket Guide” pode ser localizado pelo ISBN conhecido.

---

### User Story 2 - Consultar um livro por ISBN (Priority: P2)

Como profissional de qualidade, quero consultar um livro específico por ISBN para validar que o detalhe retornado é coerente com o catálogo.

**Why this priority**: Introduz parâmetros de consulta e comparação entre dois contratos públicos sem exigir autenticação ou alteração de dados.

**Independent Test**: Consultar o ISBN conhecido e confirmar sucesso, conteúdo JSON e correspondência exata dos principais dados do livro.

**Acceptance Scenarios**:

1. **Given** um ISBN existente, **When** o detalhe é consultado, **Then** a resposta apresenta o mesmo ISBN, título e autor esperados.
2. **Given** o livro presente no catálogo, **When** seu detalhe é consultado, **Then** seus dados essenciais são coerentes com o item listado.

---

### User Story 3 - Rejeitar ISBN inexistente (Priority: P3)

Como profissional de qualidade, quero consultar um ISBN inexistente para validar o contrato de erro e diferenciar entrada sem correspondência de falha técnica.

**Why this priority**: Completa o primeiro conjunto com um cenário negativo objetivo, mas não bloqueia o aprendizado dos fluxos positivos.

**Independent Test**: Consultar um ISBN de 13 dígitos que não pertence ao catálogo e confirmar status de requisição inválida e mensagem de domínio identificável.

**Acceptance Scenarios**:

1. **Given** um ISBN bem formado, porém inexistente, **When** o detalhe é consultado, **Then** a resposta indica requisição inválida e informa que o ISBN não está disponível.
2. **Given** uma resposta de erro, **When** seu conteúdo é inspecionado, **Then** existe um código de erro de domínio e uma mensagem textual não vazia.

### Edge Cases

- O catálogo externo pode ficar indisponível ou lento sem que exista defeito no código de teste.
- Uma alteração legítima no livro de referência pode exigir atualização prévia da especificação e do contrato.
- A resposta com sucesso, mas sem conteúdo JSON compatível, deve falhar como quebra de contrato.
- Um ISBN inexistente deve ser diferente de ausência do parâmetro; somente o primeiro caso pertence a esta fase.
- Nenhum cenário deve criar usuário, gerar token, autenticar ou modificar coleções públicas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A validação MUST consultar publicamente a coleção de livros e confirmar resposta de sucesso.
- **FR-002**: A resposta do catálogo MUST declarar conteúdo JSON e apresentar uma coleção não vazia.
- **FR-003**: Os livros validados MUST apresentar ISBN, título, autor, editora e quantidade de páginas em formatos compatíveis.
- **FR-004**: O catálogo MUST conter o livro de referência identificado pelo ISBN `9781449325862`.
- **FR-005**: A validação MUST permitir consultar individualmente um livro por ISBN.
- **FR-006**: O detalhe do livro de referência MUST apresentar ISBN, título e autor coerentes com o catálogo.
- **FR-007**: A consulta de um ISBN inexistente MUST retornar uma resposta de requisição inválida.
- **FR-008**: A resposta de ISBN inexistente MUST conter código de domínio e mensagem textual útil.
- **FR-009**: Cada cenário MUST ser independente, somente leitura e não MUST exigir credenciais.
- **FR-010**: A suíte de API MUST permanecer separada das suítes de interface local e externa e somente acessar o serviço remoto quando solicitada explicitamente.
- **FR-011**: Falhas MUST preservar informações de requisição, resposta e asserção suficientes para diagnóstico, sem registrar segredos.

### Key Entities

- **Book Collection**: Resposta que agrupa os livros disponíveis no catálogo público.
- **Book**: Livro identificado por ISBN, com título, subtítulo, autor, editora, páginas, descrição, data de publicação e website.
- **API Error**: Resposta de falha contendo código de domínio e mensagem explicativa.
- **Reference Book**: Livro conhecido usado para comparar catálogo e detalhe nesta fase.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um estudante executa a primeira consulta automatizada da API em até 5 minutos seguindo somente o quickstart.
- **SC-002**: 100% dos três cenários priorizados podem ser executados e avaliados de forma independente.
- **SC-003**: Catálogo, detalhe e erro produzem resultados objetivos por status, tipo de conteúdo e corpo, sem inspeção manual obrigatória.
- **SC-004**: A coerência entre catálogo e detalhe é confirmada para 100% dos campos essenciais definidos nesta fase.
- **SC-005**: A suíte de API pode ser executada sem iniciar navegador, servidor local, autenticação ou fluxo de interface.
- **SC-006**: Quando o serviço está disponível, cada cenário termina em até 30 segundos.

## Assumptions

- O serviço público do DemoQA continua disponível em `https://demoqa.com` e pode sofrer alterações fora do controle do projeto.
- O livro “Git Pocket Guide”, ISBN `9781449325862`, permanece disponível como dado de referência.
- O ISBN inexistente `0000000000000` é reservado apenas para consulta negativa e não representa um livro real do catálogo.
- Esta fase cobre somente operações GET públicas do domínio de livros.
- Cadastro, autenticação, geração de token e operações POST, PUT ou DELETE serão tratados em feature posterior com estratégia segura para dados temporários.
- Os testes de API complementam os testes de interface; não os substituem.
