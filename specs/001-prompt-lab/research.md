# Research: Laboratório Local de Prompts

## CLI antes de interface web

**Decision**: começar com uma interface de linha de comando.

**Rationale**: reduz dependências e permite observar claramente entradas, saídas e códigos de
erro enquanto o estudante aprende SDD.

**Alternatives considered**: interface web foi adiada porque adicionaria servidor, frontend e
testes de navegador sem aumentar o aprendizado central desta feature.

## Provedor simulado primeiro

**Decision**: usar um provedor local determinístico nesta feature.

**Rationale**: testes ficam rápidos, gratuitos e reproduzíveis. A fronteira de provedor prepara
uma futura integração real sem torná-la requisito prematuro.

**Alternatives considered**: chamar diretamente um serviço externo exigiria chave, rede,
tratamento de custos e mocks antes de validar o fluxo básico.

## JSON Lines para histórico

**Decision**: armazenar um objeto JSON por linha.

**Rationale**: o formato é legível, acrescenta registros sem reescrever todo o arquivo e pode
ser inspecionado com ferramentas comuns.

**Alternatives considered**: banco relacional é excessivo para 1.000 registros locais; um único
array JSON exigiria reescrita integral a cada experimento.

## Biblioteca padrão em runtime

**Decision**: não adicionar dependências externas nesta fase.

**Rationale**: simplifica instalação e deixa visíveis os conceitos de domínio, persistência e
testes. Dependências futuras deverão resolver requisitos reais.

**Alternatives considered**: frameworks de CLI e validação oferecem conveniência, mas não são
necessários para três comandos pequenos.
