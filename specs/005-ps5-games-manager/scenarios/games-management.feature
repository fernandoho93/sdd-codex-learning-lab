# language: pt
Funcionalidade: Gerenciar coleção pessoal de jogos de PS5
  Como usuário local
  Quero cadastrar e acompanhar meus jogos
  Para manter minha coleção organizada

  Cenário: Cadastrar um jogo com sucesso
    Dado que a coleção está vazia
    Quando cadastro um jogo com todos os campos obrigatórios válidos
    Então o jogo é exibido na coleção com uma mensagem de sucesso

  Cenário: Impedir cadastro sem campos obrigatórios
    Dado que abri o formulário de cadastro
    Quando tento salvar sem nome, gênero, tipo de mídia ou status
    Então os campos obrigatórios são identificados e nenhum jogo é criado

  Cenário: Impedir cadastro duplicado
    Dado que existe o jogo "Astro Bot"
    Quando tento cadastrar "astro bot"
    Então recebo uma mensagem de duplicidade e a coleção mantém um registro

  Cenário: Listar jogos cadastrados
    Dado que cadastrei mais de um jogo
    Quando abro a coleção
    Então todos são listados em ordem consistente

  Cenário: Pesquisar um jogo pelo nome
    Dado que existem jogos com nomes diferentes
    Quando pesquiso por parte de um nome
    Então somente os jogos correspondentes são exibidos

  Cenário: Filtrar jogos por gênero
    Dado que existem jogos de gêneros diferentes
    Quando seleciono um gênero
    Então somente jogos desse gênero são exibidos

  Cenário: Filtrar jogos por status
    Dado que existem jogos com status diferentes
    Quando seleciono um status
    Então somente jogos desse status são exibidos

  Cenário: Editar um jogo
    Dado que existe um jogo cadastrado
    Quando altero seu status e sua nota com valores válidos
    Então os novos dados são exibidos e persistidos

  Cenário: Excluir um jogo após confirmação
    Dado que existe um jogo cadastrado
    Quando solicito e confirmo sua exclusão
    Então o jogo deixa de aparecer na coleção

  Cenário: Cancelar a exclusão
    Dado que existe um jogo cadastrado
    Quando solicito e cancelo sua exclusão
    Então o jogo permanece na coleção

  Cenário: Exibir mensagem quando não existem jogos
    Dado que nenhum jogo foi cadastrado
    Quando abro a coleção
    Então vejo uma orientação para cadastrar o primeiro jogo

  Cenário: Tratar indisponibilidade da API local
    Dado que a consulta de jogos falhar
    Quando a página tenta carregar a coleção
    Então vejo uma mensagem recuperável sem dados antigos apresentados como novos

  Cenário: Preencher cadastro pelo catálogo RAWG
    Dado que o catálogo retorna um jogo compatível com PS5
    Quando seleciono o resultado externo
    Então o formulário é preenchido, permanece editável e exibe atribuição antes de salvar

  Cenário: Continuar manualmente quando RAWG está indisponível
    Dado que o catálogo RAWG não está configurado
    Quando tento pesquisar um título externo
    Então sou orientado a continuar com o cadastro manual
