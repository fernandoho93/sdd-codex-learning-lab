# Web UI Contract: PS5 Games Manager

## Page shell

- Título `PS5 Games Manager` e ação `Cadastrar jogo`.
- Região de mensagens com anúncio acessível para sucesso e erro.
- Conteúdo utilizável por teclado e sem rolagem horizontal em 360 px.

## Collection

- Pesquisa identificada como `Pesquisar por nome`.
- Filtros identificados como `Gênero` e `Status` e ação `Limpar filtros`.
- Lista ou grade de jogos com nome, gênero, status, mídia e ações de detalhes/edição/exclusão.
- Estado inicial de carregamento, estado `Nenhum jogo cadastrado.` e estado
  `Nenhum jogo corresponde à pesquisa e aos filtros.`.

## Create and edit form

- Campos obrigatórios: `Nome`, `Gênero`, `Tipo de mídia`, `Status`.
- Opcionais: descrição, desenvolvedora, publicadora, lançamento, nota, URL da capa e observações.
- Erros associados aos campos e resumo anunciado.
- Botão de salvamento desabilitado enquanto a operação está em andamento.
- Falha preserva os valores válidos; sucesso fecha ou redefine o formulário e atualiza a coleção.

## Details

- Região ou diálogo com título contendo o nome do jogo.
- Exibe todos os campos, timestamps e alternativa textual de capa.
- Foco é movido ao título/diálogo e retorna ao controle de origem ao fechar.

## Delete confirmation

- Diálogo identifica o jogo e informa que a remoção é definitiva.
- Ações `Cancelar` e `Excluir jogo` são distintas.
- Cancelar não chama a API. Confirmar bloqueia repetição, comunica resultado e atualiza a lista.

## Public catalog

- Campo `Pesquisar no catálogo RAWG` disponível no formulário.
- Consulta apresenta carregamento independente do salvamento local.
- Cada candidato exibe nome, lançamento, gênero, capa/alternativa e ação `Usar estes dados`.
- Aplicar candidato preenche apenas valores disponíveis e não salva automaticamente.
- Dados e imagens externos exibem `Dados e imagens fornecidos por RAWG` com vínculo ativo.
- Jogos salvos que preservam dados ou capa RAWG continuam exibindo a atribuição na coleção e nos detalhes.
- Falha ou ausência de configuração informa que o cadastro manual continua disponível.
