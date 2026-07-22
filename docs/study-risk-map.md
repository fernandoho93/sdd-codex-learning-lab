# Mapa simples de riscos do estudo

**Data**: 2026-07-22  
**Escopo**: Evidência exigida no módulo 1

| Risco | Probabilidade | Impacto | Controle atual | Ação pendente |
|-------|---------------|---------|---------------|---------------|
| Pedido vago levar a uma solução diferente da intenção do estudante | Alta | Alto | Objetivo, contexto, limites e conclusão devem aparecer na instrução estruturada | Produzir e comparar as duas rodadas do exercício do módulo 1 |
| Avançar de módulo sem a evidência exigida | Alta | Alto | Status e pendências ficam visíveis no diário | Revisar o gate antes de iniciar cada módulo |
| Antecipar ferramenta, arquitetura ou testes durante a descoberta | Alta | Médio | `problem-brief.md` separa problema de solução | Revisar o texto com o estudante |
| Alterar arquivos além do escopo autorizado | Média | Alto | Comparação das alterações e revisão humana | Conferir o diff antes de aceitar ou versionar |
| Não conseguir reverter a experiência | Alta | Alto | Nenhum controle suficiente no estado atual | Estabelecer linha de base Git limpa antes do próximo exercício prático |
| Confundir indisponibilidade externa com defeito da mudança | Média | Médio | Dependência externa está explícita na descoberta | Definir tratamento observável em módulo posterior |
| Gerar muitas chamadas contra um serviço público | Baixa | Médio | Escopo de baixo volume e sem carga | Definir limite objetivo antes da implementação |
| Tratar hipótese como requisito confirmado | Média | Alto | Hipóteses e perguntas possuem seções próprias | Registrar confirmação ou rejeição após revisão humana |

## Quando exigir planejamento

O planejamento deve ser obrigatório quando ocorrer pelo menos uma destas condições:

- a mudança afetar mais de um componente ou tipo de teste;
- houver dependência externa, dado persistente ou risco de efeito colateral;
- existirem duas ou mais soluções plausíveis com consequências diferentes;
- o resultado não puder ser validado por um comando ou evidência objetiva;
- o escopo não puder ser explicado de forma curta e inequívoca;
- a reversão não estiver clara.

## Quando exigir revisão humana

A revisão humana deve ocorrer antes de modificar arquivos quando:

- houver pergunta aberta que altere escopo, resultado ou risco;
- o agente precisar assumir uma regra de negócio não documentada;
- uma ação puder publicar, excluir, sobrescrever ou expor dados;
- a solução proposta ultrapassar o módulo atual da trilha;
- a comparação de alterações incluir arquivos não relacionados à demanda;
- os critérios de conclusão não puderem ser avaliados objetivamente.

