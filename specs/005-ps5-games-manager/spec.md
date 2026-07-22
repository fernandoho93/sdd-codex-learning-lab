# Especificação da Feature: PS5 Games Manager

**Feature Branch**: `005-ps5-games-manager`

**Created**: 2026-07-22

**Status**: Ready

**Input**: Criar um sistema local, responsivo e de usuário único para cadastrar e gerenciar uma coleção de jogos de PlayStation 5, com persistência, API, interface web, documentação e testes implementados somente após o sistema estar funcional.

## Objective and Context

O PS5 Games Manager permite que uma pessoa mantenha um catálogo pessoal de jogos de
PlayStation 5 e acompanhe o interesse, a aquisição e o progresso em cada título. O MVP deve
concentrar em operações de cadastro, consulta, edição, exclusão, pesquisa e filtros, sem exigir
autenticação. Quando um catálogo público estiver configurado e disponível, o usuário também
pode pesquisar um jogo externo para preencher o formulário, mantendo o cadastro manual como
alternativa completa.

Atualmente o projeto não oferece uma forma de organizar jogos. Esta feature cria um sistema
independente do Prompt Lab existente, mas segue o mesmo processo orientado por especificações,
com incrementos demonstráveis e rastreabilidade entre histórias, requisitos, tarefas e
validações.

## Scope

### In Scope

- Cadastrar um jogo com os dados definidos nesta especificação.
- Listar todos os jogos em uma organização clara e responsiva.
- Consultar os detalhes completos de um jogo.
- Editar um jogo existente.
- Excluir um jogo depois de confirmação explícita.
- Pesquisar jogos por parte do nome.
- Filtrar jogos por gênero e status, inclusive em combinação com a pesquisa.
- Persistir os dados entre reinicializações do sistema.
- Validar entradas tanto na interface quanto na fronteira de serviço.
- Comunicar carregamento, sucesso, ausência de dados e erros recuperáveis.
- Expor as operações do sistema por um contrato de serviço documentado.
- Pesquisar jogos de PS5 em um catálogo público opcional para preencher dados do formulário.
- Permitir revisar e editar todos os dados externos antes de persistir um jogo.
- Exibir a atribuição exigida pela fonte pública quando dados ou imagens dela forem utilizados.
- Documentar execução, configuração, uso, limitações e validação.

### Out of Scope

- Autenticação, autorização, contas ou múltiplos usuários.
- Sincronização entre dispositivos ou armazenamento em nuvem.
- Sincronização contínua com catálogo externo ou atualização automática de jogos já salvos.
- Funcionamento do catálogo público sem conexão, credenciais válidas ou disponibilidade do provedor.
- Compra, venda, empréstimo, preço ou controle financeiro.
- Avaliações públicas, recursos sociais ou compartilhamento de coleção.
- Jogos de outras plataformas.
- Upload e armazenamento local de imagens de capa.
- Paginação, ordenação personalizada e relatórios avançados no MVP.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cadastrar e consultar jogos (Priority: P1)

Como colecionador de jogos de PS5, quero cadastrar um jogo e encontrá-lo na coleção para
manter um registro confiável dos títulos que acompanho.

**Why this priority**: O cadastro persistente e a consulta formam o menor fluxo que entrega
valor e sustentam todas as demais operações do sistema.

**Independent Test**: Iniciar com uma coleção vazia, cadastrar um jogo somente com os campos
obrigatórios, reiniciar o sistema, localizar o registro na listagem e abrir seus detalhes.

**Acceptance Scenarios**:

1. **Given** uma coleção vazia, **When** o usuário cadastra nome, gênero, tipo de mídia e status válidos, **Then** o jogo é persistido, uma confirmação é exibida e o registro aparece na listagem.
2. **Given** um jogo cadastrado, **When** o usuário abre seus detalhes, **Then** todos os dados informados e os metadados de criação e atualização são apresentados.
3. **Given** nenhum jogo cadastrado, **When** a listagem é aberta, **Then** um estado vazio orienta o usuário a cadastrar o primeiro jogo.
4. **Given** um formulário sem algum campo obrigatório, **When** o usuário tenta salvar, **Then** os campos inválidos são identificados e nenhum registro é criado.
5. **Given** um jogo chamado `Astro Bot`, **When** o usuário tenta cadastrar `astro bot`, **Then** o cadastro é rejeitado como duplicado com uma mensagem clara.

---

### User Story 2 - Pesquisar e filtrar a coleção (Priority: P2)

Como usuário com vários jogos, quero pesquisar por nome e filtrar por gênero e status para
encontrar rapidamente os títulos relevantes.

**Why this priority**: A descoberta eficiente aumenta o valor da coleção depois que já há
registros persistidos, sem ser necessária para o primeiro cadastro.

**Independent Test**: Preparar jogos com nomes, gêneros e status diferentes e verificar os
resultados de pesquisa, de cada filtro e da combinação entre eles.

**Acceptance Scenarios**:

1. **Given** jogos com nomes diferentes, **When** o usuário pesquisa por parte de um nome sem considerar maiúsculas e minúsculas, **Then** somente os jogos correspondentes são exibidos.
2. **Given** jogos de gêneros diferentes, **When** o usuário escolhe um gênero, **Then** somente os jogos daquele gênero são exibidos.
3. **Given** jogos com status diferentes, **When** o usuário escolhe um status, **Then** somente os jogos naquele status são exibidos.
4. **Given** pesquisa e filtros preenchidos, **When** eles são aplicados em conjunto, **Then** somente jogos que atendem a todos os critérios são exibidos.
5. **Given** nenhum jogo compatível, **When** o resultado é apresentado, **Then** a interface diferencia uma busca sem resultados de uma coleção vazia e permite limpar os critérios.

---

### User Story 3 - Atualizar informações e progresso (Priority: P3)

Como colecionador, quero editar os dados e o status de um jogo para manter a coleção atualizada
à medida que compro e jogo os títulos.

**Why this priority**: A atualização preserva a utilidade do catálogo ao longo do tempo, mas
depende da existência de um jogo previamente cadastrado.

**Independent Test**: Editar dados de um jogo conhecido, confirmar a alteração na listagem e
nos detalhes e verificar que a data de atualização mudou sem alterar a data de criação.

**Acceptance Scenarios**:

1. **Given** um jogo cadastrado, **When** o usuário altera campos com valores válidos, **Then** as mudanças são persistidas e uma confirmação é exibida.
2. **Given** uma edição que remove um campo obrigatório ou informa nota inválida, **When** o usuário tenta salvar, **Then** a edição é rejeitada e o registro anterior permanece íntegro.
3. **Given** dois jogos diferentes, **When** uma edição faria seus nomes se tornarem duplicados, **Then** a edição é rejeitada e ambos permanecem inalterados.

---

### User Story 4 - Excluir um jogo com segurança (Priority: P4)

Como usuário, quero excluir um jogo que não desejo mais acompanhar, com confirmação, para
evitar remoções acidentais.

**Why this priority**: A exclusão completa o gerenciamento, mas pode ser entregue depois dos
fluxos de criação, descoberta e atualização.

**Independent Test**: Solicitar a exclusão de um jogo, cancelar e confirmar que ele permanece;
repetir, confirmar a exclusão e verificar que ele não pode mais ser listado nem consultado.

**Acceptance Scenarios**:

1. **Given** um jogo cadastrado, **When** o usuário solicita sua exclusão, **Then** o sistema apresenta uma confirmação que identifica claramente o jogo.
2. **Given** uma confirmação aberta, **When** o usuário cancela, **Then** o jogo permanece sem alterações.
3. **Given** uma confirmação aberta, **When** o usuário confirma, **Then** o jogo é removido, uma mensagem de sucesso é exibida e ele deixa de aparecer na coleção.
4. **Given** um jogo que já não existe, **When** sua exclusão é solicitada, **Then** o sistema apresenta um erro recuperável e atualiza a visão da coleção.

---

### User Story 5 - Preencher um cadastro pelo catálogo público (Priority: P5)

Como usuário, quero pesquisar um título em um catálogo público para aproveitar nome, gênero,
descrição, empresas, lançamento e capa sem precisar digitar todos esses dados manualmente.

**Why this priority**: O enriquecimento reduz trabalho, mas não pode bloquear o gerenciamento
principal nem tornar os dados locais dependentes de um terceiro.

**Independent Test**: Usar uma resposta externa controlada para pesquisar um jogo disponível
no PlayStation 5, selecionar um resultado, revisar os campos preenchidos e salvá-lo; repetir
com indisponibilidade externa e concluir um cadastro manual.

**Acceptance Scenarios**:

1. **Given** um catálogo público configurado e disponível, **When** o usuário pesquisa um título, **Then** o sistema apresenta somente resultados identificados como compatíveis com PlayStation 5 e mostra sua fonte.
2. **Given** um resultado externo selecionado, **When** o usuário o aplica ao formulário, **Then** os campos compatíveis são preenchidos sem salvar automaticamente o jogo.
3. **Given** dados externos preenchidos, **When** o usuário os revisa e altera, **Then** a versão editada pelo usuário é a que será validada e persistida.
4. **Given** uma resposta sem correspondências, **When** a pesquisa termina, **Then** o sistema comunica a ausência de resultados e mantém disponível o cadastro manual.
5. **Given** credencial ausente, limite excedido, timeout, falha de rede ou erro do provedor, **When** a consulta externa falha, **Then** uma mensagem recuperável é exibida e o CRUD local continua disponível.
6. **Given** dados ou imagens provenientes do catálogo público, **When** eles são apresentados, **Then** a atribuição e o vínculo exigidos pela fonte permanecem visíveis.

### Edge Cases

- Nomes e gêneros contendo caracteres acentuados devem ser preservados e pesquisáveis.
- Espaços externos dos campos textuais são removidos antes da validação e persistência.
- Um nome contendo somente espaços é considerado vazio.
- Datas de lançamento futuras são aceitas para jogos que o usuário deseja comprar.
- Uma URL de capa ausente é aceita; quando informada, deve representar um endereço HTTP ou HTTPS completo.
- Uma nota ausente é aceita; quando informada, deve pertencer à escala definida nas regras de negócio.
- Pesquisa vazia equivale a não pesquisar, e filtros vazios equivalem a não filtrar.
- Filtros desconhecidos ou valores fora das opções permitidas são rejeitados, sem resultados silenciosamente incorretos.
- Falhas de leitura ou gravação não podem ser apresentadas como sucesso nem descartar dados já persistidos.
- Textos longos e URLs de capa inválidas não podem quebrar o layout ou impedir a recuperação do formulário.
- Cliques repetidos enquanto um salvamento está em andamento não devem criar registros duplicados.
- Identificadores inexistentes ou malformados devem produzir uma resposta segura e compreensível.
- Resultados externos sem todos os campos devem preencher apenas valores disponíveis e deixar os demais editáveis.
- Um resultado externo para múltiplas plataformas só pode ser oferecido quando incluir PlayStation 5.
- Conteúdo textual, URLs e identificadores externos devem ser tratados como entrada não confiável.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST permitir cadastrar um jogo com nome, gênero, tipo de mídia e status.
- **FR-002**: O sistema MUST aceitar descrição, desenvolvedora, publicadora, data de lançamento, nota pessoal, URL da capa e observações como dados opcionais.
- **FR-003**: O sistema MUST gerar um identificador único e registrar datas de criação e última atualização para cada jogo.
- **FR-004**: O sistema MUST impedir nomes duplicados após remover espaços externos e desconsiderar diferenças entre letras maiúsculas e minúsculas.
- **FR-005**: O sistema MUST validar todas as entradas na fronteira de serviço, independentemente das validações realizadas pela interface.
- **FR-006**: O sistema MUST listar todos os jogos persistidos e permitir a abertura dos detalhes completos de cada registro.
- **FR-007**: O sistema MUST permitir editar todos os dados informados pelo usuário sem alterar o identificador nem a data de criação.
- **FR-008**: O sistema MUST atualizar a data da última alteração somente quando uma edição válida for persistida.
- **FR-009**: O sistema MUST solicitar confirmação explícita antes de excluir um jogo pela interface.
- **FR-010**: O sistema MUST excluir definitivamente um jogo somente após a confirmação do usuário.
- **FR-011**: O sistema MUST pesquisar por correspondência parcial do nome sem considerar maiúsculas e minúsculas.
- **FR-012**: O sistema MUST filtrar jogos por gênero e por um dos status permitidos.
- **FR-013**: O sistema MUST combinar pesquisa, gênero e status usando todos os critérios fornecidos.
- **FR-014**: O sistema MUST persistir alterações para que os dados permaneçam disponíveis após seu reinício.
- **FR-015**: O sistema MUST apresentar estados distintos para carregamento, sucesso, coleção vazia, busca sem resultados e falha.
- **FR-016**: O sistema MUST impedir envios repetidos enquanto uma criação, edição ou exclusão estiver em andamento.
- **FR-017**: O sistema MUST retornar falhas de serviço em um formato consistente contendo código estável, mensagem legível e detalhes de campos quando aplicável.
- **FR-018**: O sistema MUST diferenciar pelo menos dados inválidos, duplicidade, registro inexistente e falha interna.
- **FR-019**: O sistema MUST permitir limpar pesquisa e filtros para recuperar a listagem completa.
- **FR-020**: A interface MUST ser utilizável em telas estreitas e largas sem perda de controles ou conteúdo essencial.
- **FR-021**: Controles, formulários, mensagens, confirmação e detalhes MUST possuir nomes compreensíveis e ser operáveis por teclado.
- **FR-022**: O sistema MUST preservar os dados válidos já preenchidos quando uma operação de formulário falhar.
- **FR-023**: O sistema MUST apresentar uma alternativa textual quando a capa estiver ausente ou não puder ser exibida.
- **FR-024**: O sistema MUST permitir pesquisar jogos em um catálogo público quando a integração estiver configurada.
- **FR-025**: A pesquisa externa MUST restringir ou identificar resultados compatíveis com PlayStation 5.
- **FR-026**: Selecionar um resultado externo MUST apenas preencher o formulário; o jogo só pode ser persistido após revisão e confirmação do usuário.
- **FR-027**: Todos os valores externos MUST passar pelas mesmas validações aplicadas ao cadastro manual.
- **FR-028**: A indisponibilidade da integração externa MUST preservar cadastro, consulta, edição, exclusão, pesquisa e filtros locais.
- **FR-029**: O sistema MUST apresentar atribuição e vínculo para a fonte externa sempre que seus dados ou imagens forem exibidos.
- **FR-030**: Credenciais da integração MUST ser opcionais para o funcionamento local e nunca podem ser apresentadas na interface, mensagens ou respostas de erro.

### Non-Functional Requirements

- **NFR-001**: Operações locais de listagem, pesquisa e filtros com até 5.000 jogos MUST apresentar o resultado ao usuário em até 2 segundos em um ambiente de desenvolvimento compatível.
- **NFR-002**: Criação, consulta, edição e exclusão MUST produzir o mesmo resultado para a mesma entrada e estado inicial, sem depender de serviços externos.
- **NFR-003**: Mensagens MUST explicar como o usuário pode corrigir entradas inválidas ou tentar novamente após uma falha recuperável.
- **NFR-004**: Dados gerados pelo usuário MUST permanecer locais no MVP e não podem ser enviados a terceiros.
- **NFR-005**: As operações MUST preservar a integridade do registro anterior quando uma validação ou persistência falhar.
- **NFR-006**: A documentação MUST permitir que uma pessoa com os pré-requisitos declarados prepare, execute e valide o sistema seguindo somente o quickstart.
- **NFR-007**: Consultas ao catálogo externo MUST possuir limite de duração e falhar de forma recuperável, sem bloquear indefinidamente a interface.
- **NFR-008**: Testes automatizados MUST simular a integração externa e não depender da disponibilidade, cota ou credencial real do provedor.

### Business Rules

- **BR-001**: Nome, gênero, tipo de mídia e status são obrigatórios.
- **BR-002**: O tipo de mídia aceita exclusivamente `física` ou `digital`.
- **BR-003**: O status aceita exclusivamente `desejo comprar`, `comprado`, `jogando`, `concluído` ou `abandonado`.
- **BR-004**: A nota pessoal é opcional e, quando informada, aceita valores de `0,0` a `10,0`, inclusive, em incrementos de `0,5`.
- **BR-005**: O nome deve conter de 1 a 200 caracteres após normalização de espaços externos.
- **BR-006**: O gênero deve conter de 1 a 100 caracteres após normalização de espaços externos.
- **BR-007**: Descrição e observações aceitam respectivamente até 2.000 e 5.000 caracteres.
- **BR-008**: Desenvolvedora e publicadora aceitam até 200 caracteres cada.
- **BR-009**: A URL da capa deve ter no máximo 2.048 caracteres e usar HTTP ou HTTPS quando informada.
- **BR-010**: A data de lançamento é opcional, representa uma data de calendário válida e pode estar no futuro.
- **BR-011**: A comparação de duplicidade não considera maiúsculas, minúsculas nem espaços externos, mas preserva o nome digitado para exibição.
- **BR-012**: O gênero é texto livre no cadastro; os filtros disponíveis são derivados dos gêneros existentes e comparados sem considerar maiúsculas e minúsculas.

### Service Contract Requirements

- **CR-001**: O contrato MUST oferecer operações para criar, listar, consultar por identificador, atualizar e excluir jogos.
- **CR-002**: A listagem MUST aceitar pesquisa opcional por nome e filtros opcionais por gênero e status.
- **CR-003**: Uma criação bem-sucedida MUST devolver o registro completo persistido.
- **CR-004**: Uma consulta ou atualização bem-sucedida MUST devolver o registro completo correspondente.
- **CR-005**: Uma exclusão bem-sucedida MUST confirmar a remoção sem devolver um registro inexistente como se ainda estivesse disponível.
- **CR-006**: Entradas inválidas MUST identificar os campos rejeitados sem expor detalhes internos do sistema.
- **CR-007**: Nomes duplicados e identificadores inexistentes MUST ser distinguíveis por consumidores do contrato.
- **CR-008**: A especificação detalhada do contrato MUST incluir exemplos de entrada, saída, filtros e falhas antes da implementação.
- **CR-009**: O contrato MUST oferecer uma operação de pesquisa no catálogo externo sem expor a credencial ao navegador.
- **CR-010**: Respostas da pesquisa externa MUST apresentar somente os campos necessários ao preenchimento e a informação de atribuição.
- **CR-011**: Falhas externas MUST ser distinguíveis de falhas do armazenamento local.

### Key Entities

- **Game**: Um jogo acompanhado pelo usuário. Possui identificador, nome, descrição, gênero, desenvolvedora, publicadora, data de lançamento, tipo de mídia, status, nota pessoal, URL da capa, observações, origem externa opcional, data de criação e data da última atualização.
- **Media Type**: Classificação controlada que distingue uma cópia física de uma licença digital.
- **Game Status**: Estado atual do interesse ou progresso do usuário: desejo comprar, comprado, jogando, concluído ou abandonado.
- **Game Query**: Conjunto transitório e não persistido de pesquisa por nome e filtros por gênero e status.
- **Interface State**: Estado transitório e não persistido da experiência: inicial, carregando, sucesso, vazio, sem resultados ou erro.
- **Service Error**: Representação consistente de uma falha, contendo código, mensagem e detalhes opcionais de campos.
- **External Game Candidate**: Resultado transitório e não persistido do catálogo público, limitado a jogos compatíveis com PlayStation 5 e aos campos úteis para preencher o formulário.
- **External Attribution**: Fonte, vínculo e texto que devem acompanhar dados ou imagens externos conforme as condições do provedor.

## User Flows

### Cadastro e consulta

1. O usuário abre a coleção e visualiza os jogos ou o estado vazio.
2. O usuário abre o formulário de cadastro.
3. O sistema valida os campos e indica correções sem apagar dados válidos.
4. Uma entrada válida é persistida e confirmada.
5. O novo jogo aparece na coleção e pode ter seus detalhes abertos.

### Pesquisa e filtros

1. O usuário informa parte de um nome e/ou seleciona gênero e status.
2. A coleção comunica que a consulta está em andamento quando houver espera perceptível.
3. O sistema apresenta apenas os jogos que atendem a todos os critérios.
4. Sem correspondências, o usuário recebe orientação para limpar ou alterar os critérios.

### Edição

1. O usuário abre um jogo existente e solicita a edição.
2. O formulário apresenta os valores atuais.
3. O sistema rejeita alterações inválidas ou duplicadas preservando o registro anterior.
4. Uma alteração válida é persistida, confirmada e refletida na coleção e nos detalhes.

### Exclusão

1. O usuário solicita a exclusão de um jogo identificado por nome.
2. O sistema pede confirmação explícita.
3. Cancelar mantém o jogo; confirmar remove o registro.
4. O sistema comunica o resultado e atualiza a coleção.

### Preenchimento pelo catálogo público

1. O usuário abre o cadastro e pesquisa um título no catálogo público.
2. O sistema apresenta carregamento, resultados compatíveis com PS5 e a atribuição da fonte.
3. O usuário seleciona um resultado e recebe um formulário preenchido, ainda não salvo.
4. O usuário revisa, corrige ou completa os campos e confirma o cadastro local.
5. Se a integração falhar, o sistema explica a indisponibilidade e mantém o formulário manual utilizável.

## Interface States

- **Initial**: Estrutura pronta antes da primeira consulta.
- **Loading**: Operação em andamento, controles conflitantes temporariamente indisponíveis e estado anunciado sem depender apenas de cor.
- **Success**: Operação concluída com mensagem específica e visão atualizada.
- **Empty Collection**: Nenhum jogo cadastrado, com ação clara para iniciar um cadastro.
- **No Results**: Existem jogos, mas nenhum corresponde à pesquisa ou aos filtros; oferece limpeza dos critérios.
- **Validation Error**: Campos rejeitados identificados junto aos controles e por uma mensagem resumida.
- **Operational Error**: Falha recuperável com opção de tentar novamente e sem apresentar dados antigos como novos.
- **Delete Confirmation**: Nome do jogo, consequência da ação e opções inequívocas de confirmar ou cancelar.
- **External Search Loading**: Consulta externa em andamento, com possibilidade de recuperação após timeout ou falha.
- **External Search Results**: Resultados compatíveis com PS5, fonte identificada e ação explícita para preencher o formulário.
- **External Search Unavailable**: Falha do catálogo isolada do CRUD local, com orientação para continuar manualmente.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um usuário consegue cadastrar seu primeiro jogo válido e encontrá-lo na coleção em até 2 minutos, sem consultar documentação técnica.
- **SC-002**: 100% das criações e edições confirmadas permanecem disponíveis após reiniciar o sistema.
- **SC-003**: 100% das tentativas sem campos obrigatórios, com nota inválida ou com nome duplicado são rejeitadas sem alterar registros existentes.
- **SC-004**: Pesquisa e filtros apresentam o conjunto correto em até 2 segundos para uma coleção de até 5.000 jogos.
- **SC-005**: Todos os 12 fluxos mínimos de automação definidos para o MVP possuem cenários executáveis e resultados determinísticos antes da conclusão da feature.
- **SC-006**: Todas as operações essenciais — cadastrar, listar, detalhar, pesquisar, filtrar, editar e excluir — podem ser concluídas usando somente teclado.
- **SC-007**: Em larguras equivalentes a celular e desktop, nenhum controle essencial exige rolagem horizontal e nenhum conteúdo impede a conclusão dos fluxos principais.
- **SC-008**: 100% das falhas previstas apresentam uma mensagem que distingue validação, duplicidade, ausência de registro ou indisponibilidade operacional.
- **SC-009**: Um usuário consegue pesquisar, selecionar, revisar e cadastrar um jogo do catálogo público em até 2 minutos quando a integração está disponível.
- **SC-010**: 100% dos fluxos locais essenciais continuam utilizáveis quando a integração pública está sem credencial, indisponível ou excede seu tempo limite.

## Risks and Mitigations

- **R-001 — Perda ou corrupção de dados locais**: exigir operações que preservem o estado anterior em caso de falha e incluir cenários de persistência e recuperação na estratégia de testes.
- **R-002 — Divergência entre interface e serviço**: definir um único contrato documentado e validar as mesmas regras na fronteira de serviço.
- **R-003 — Exclusão acidental**: exigir identificação do jogo e confirmação explícita antes da remoção.
- **R-004 — Crescimento de complexidade visual**: limitar o MVP às telas e estados necessários aos fluxos definidos.
- **R-005 — Dependência de capas externas**: tratar URL como opcional e sempre oferecer alternativa textual.
- **R-006 — Inconsistência de nomes e gêneros**: normalizar espaços para validação e usar comparação sem distinção entre maiúsculas e minúsculas.
- **R-007 — Indisponibilidade, cota ou mudança do catálogo público**: isolar a integração, aplicar limite de duração e preservar o cadastro manual.
- **R-008 — Licença ou atribuição inadequada**: documentar as condições do provedor e apresentar atribuição e vínculo junto a seus dados e imagens.
- **R-009 — Exposição de credencial**: realizar consultas externas por uma fronteira controlada e impedir que chaves apareçam no cliente ou em mensagens.

## Future Test Plan

Os testes serão escritos somente depois que a implementação funcional correspondente estiver
disponível, conforme solicitado para esta feature. Antes da automação end-to-end, os fluxos
principais serão registrados em Gherkin. A estratégia posterior deve cobrir:

- regras e validações isoladas do domínio;
- persistência, unicidade e preservação de dados após falhas;
- contrato e integração das operações de serviço;
- estados e comportamentos principais da interface;
- jornadas completas de cadastro, validação obrigatória, duplicidade, listagem, pesquisa,
  filtros, edição, confirmação e cancelamento de exclusão, estado vazio e falha do serviço;
- cenários positivos, negativos, de exceção e combinações de pesquisa e filtros;
- operação por teclado, mensagens acessíveis e larguras representativas de celular e desktop;
- reinicialização do sistema para comprovar persistência.
- integração externa simulada para resultados, ausência de correspondências, campos incompletos,
  timeout, falha de autenticação, limite excedido e indisponibilidade;
- comprovação de que a atribuição é exibida e de que todos os fluxos locais permanecem
  utilizáveis quando o catálogo público falha.

## Assumptions

- O MVP atende uma única pessoa em uma instalação local e não requer autenticação.
- O sistema gerencia somente jogos de PlayStation 5, inclusive títulos ainda não lançados.
- O gênero é informado como texto livre e reutilizado como opção de filtro.
- A nota pessoal segue escala de 0 a 10 em incrementos de 0,5.
- A exclusão é definitiva no MVP; lixeira e restauração permanecem fora do escopo.
- A ordenação padrão será consistente e definida no contrato durante o planejamento.
- Datas e horários de auditoria são gerados pelo sistema; o usuário informa somente a data de lançamento.
- A aplicação não verifica se uma URL de capa realmente responde, apenas se possui formato aceito.
- A integração com catálogo público é opcional em runtime, mas faz parte do escopo funcional quando configurada.
- Dados obtidos externamente são sugestões editáveis; o registro local confirmado pelo usuário é a fonte de verdade da coleção.
- Quando o usuário salva dados ou uma capa da fonte externa, a identificação e o vínculo dessa fonte permanecem associados ao jogo exclusivamente para atribuição.
- O provedor público e suas condições de uso serão escolhidos e registrados durante a pesquisa técnica.
- Decisões de linguagem, armazenamento, estrutura física, migrações e ferramentas pertencem ao plano técnico, não a esta especificação.

## Data and Privacy Boundaries

- Todos os dados do catálogo permanecem na máquina local no MVP.
- Somente o termo de pesquisa necessário pode ser enviado ao catálogo público quando o usuário acionar essa função.
- URLs de capa podem apontar para conteúdo externo e devem ser tratadas como entrada não confiável.
- Credenciais do catálogo público devem permanecer no servidor e fora do repositório, do navegador e dos registros de diagnóstico.
- O cadastro manual e todo o gerenciamento local devem funcionar sem comunicação externa.
- Segredos, dados gerados, evidências de teste e conteúdo da coleção não devem ser versionados.
