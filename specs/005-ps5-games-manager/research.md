# Research: PS5 Games Manager

## Persistência local

**Decision**: usar SQLite por meio do módulo `sqlite3` da biblioteca padrão do Python.

**Rationale**: o domínio exige unicidade, criação, leitura, atualização, exclusão, pesquisa,
filtros e evolução de esquema. SQLite fornece transações e índices em um único arquivo local,
sem serviço adicional ou dependência de runtime.

**Alternatives considered**: JSON/JSONL preservaria legibilidade direta, mas exigiria reescrita
atômica e índices próprios; PostgreSQL adicionaria instalação, credenciais e operação sem uma
necessidade de escala ou concorrência no MVP.

## Migrações

**Decision**: manter scripts SQL numerados no pacote e uma tabela `schema_migrations`.

**Rationale**: um executor pequeno aplica cada versão uma vez dentro de transação e torna a
evolução reproduzível sem biblioteca adicional.

**Alternatives considered**: criar tabelas diretamente no código esconderia o histórico;
Alembic exigiria SQLAlchemy e mais conceitos do que o MVP justifica.

## Identidade, duplicidade e pesquisa

**Decision**: gerar UUIDs e persistir chaves normalizadas com `strip().casefold()` para nome e
gênero. Um índice único protege `name_key`; pesquisa parcial usa `name_key`.

**Rationale**: `NOCASE` nativo do SQLite é limitado principalmente a ASCII. Normalizar no
domínio mantém o mesmo comportamento em validação, persistência e consulta sem perder a grafia
original exibida ao usuário.

**Alternatives considered**: IDs inteiros expõem sequência sem benefício; depender apenas de
`LOWER()` poderia divergir para Unicode; impedir apenas duplicidades exatas violaria a spec.

## Servidor e frontend

**Decision**: reutilizar `ThreadingHTTPServer`, HTML semântico, CSS responsivo e JavaScript sem
framework, em pacote separado do Prompt Lab.

**Rationale**: o repositório já valida esse desenho e o MVP possui uma entidade e poucas telas.
Compartilhar o mesmo processo elimina CORS e pipeline de build do produto.

**Alternatives considered**: FastAPI e React oferecem ecossistemas maiores, mas adicionariam
dependências e estrutura sem resolver um requisito exclusivo deste incremento.

## Catálogo público

**Decision**: usar RAWG como provedor inicial, sempre por um adaptador no backend.

**Rationale**: a API oferece pesquisa e metadados de jogos para múltiplas plataformas, incluindo
PlayStation 5, e uma chave adequada a projeto pessoal. Seus termos exigem atribuição e vínculo
quando dados ou imagens são usados; por isso a atribuição integra o contrato e a interface.

**Alternatives considered**: IGDB possui catálogo rico, mas requer cadastro Twitch, Client ID,
segredo e fluxo OAuth de aplicação; isso amplia configuração e renovação de token. Entrada
puramente manual continua como fallback, mas não atende sozinha ao pedido de API pública.

## Segurança e resiliência RAWG

**Decision**: ler `RAWG_API_KEY` somente no servidor, usar HTTPS, timeout de 5 segundos, no
máximo 10 resultados, filtro de plataforma PS5, resposta reduzida e erros externos próprios.

**Rationale**: a chave RAWG é enviada ao provedor e não pode aparecer no JavaScript, logs ou
respostas. Limites e falhas remotas não devem afetar SQLite nem as rotas locais.

**Alternatives considered**: chamada direta do navegador exporia a chave; cache persistente de
resultados externos criaria obrigações de validade e redistribuição fora do MVP.

## Estratégia de testes

**Decision**: implementar os fluxos funcionais primeiro; depois criar `unittest` com arquivos
SQLite temporários, transporte RAWG injetável e Playwright contra servidor e banco isolados.

**Rationale**: respeita a sequência explicitamente pedida pelo usuário sem abrir mão do gate
constitucional de testes verdes antes da conclusão. Cenários Gherkin precedem o E2E.

**Alternatives considered**: chamar RAWG real tornaria testes dependentes de rede, chave e cota;
usar o banco de desenvolvimento arriscaria dados pessoais.

## Acessibilidade e responsividade

**Decision**: usar formulários nativos, regiões vivas, foco gerenciado, diálogo de confirmação
acessível, layout fluido e imagens com alternativa textual.

**Rationale**: controles semânticos tornam o sistema utilizável por teclado e produzem locators
Playwright estáveis baseados na percepção do usuário.

**Alternatives considered**: componentes visuais customizados aumentariam CSS, JavaScript e
risco de acessibilidade sem ampliar o escopo funcional.

