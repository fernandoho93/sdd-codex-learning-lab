# Contrato de Interface Observável: DemoQA Books

Este contrato descreve somente comportamentos públicos que a automação pode observar. Ele não controla nem modifica o DemoQA.

## Catálogo `/books`

- A página é identificada pelo caminho `/books` e pela coluna `Title`; a versão atual do site não expõe um título principal semântico.
- Existe um campo de pesquisa identificado pelo placeholder `Type to search`.
- Um livro é representado por um título selecionável dentro da lista do catálogo.
- A consulta filtra os livros enquanto o visitante digita.
- Uma consulta sem correspondência não apresenta títulos de livros.
- Limpar a consulta restaura os livros.

## Detalhes `/books?search=<isbn>`

- Selecionar `Git Pocket Guide` abre uma página cujo parâmetro `search` identifica o ISBN do livro.
- Os valores observáveis incluem:
  - título: `Git Pocket Guide`;
  - autor: `Richard E. Silverman`;
  - ISBN: `9781449325862`.
- O controle `Back To Book Store` retorna ao catálogo.

## Fora do contrato

- Publicidade, rodapé, imagens promocionais e chamadas de terceiros.
- Ordem total, quantidade exata e paginação completa do catálogo.
- Login, cadastro, perfil e alterações de coleção.
- Tempos de resposta internos do serviço.

## Política para mudanças externas

Uma quebra deste contrato deve ser investigada primeiro com screenshot, trace e acesso manual. Se o comportamento público mudou legitimamente, a especificação e o dado de teste devem ser atualizados antes da automação.
