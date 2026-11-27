# 0005 — Média estadual da climatologia

- **Data:** 2026-11-27
- **Status:** aceita
- **Relação:** complementa o item 7 da [ADR 0004](0004-convencoes-de-agregacao.md); implementada na view `vw_climatologia_mensal_regiao` de `sql/04_views.sql` (#44)

## Contexto

O painel mostra a climatologia mensal por macro e microrregião. Sem uma região selecionada, ele ficava vazio, e a pergunta natural de quem o abre é: "e no estado como um todo?".

A rede é desigual (ADR 0004): a macrorregião Metropolitana concentra 5 das 13 estações, enquanto macrorregiões maiores, como a Norte, têm poucas. Por isso, a forma de calcular a média estadual muda o resultado.

## Decisão

1. **Cálculo em três etapas:** a climatologia de cada estação (ADR 0004, item 6), depois a de cada macrorregião (média simples das estações, item 7) e, por fim, a do **estado: média simples das climatologias das macrorregiões**. Cada macrorregião pesa o mesmo, independentemente do número de estações.
2. **Composição fixa:** o estado só tem valor num mês se **todas as macrorregiões** tiverem valor nele. Assim, a falta de uma macrorregião não muda silenciosamente a composição da média, pelo mesmo princípio da ADR 0004.
3. **Transparência:** o número de estações do estado é a soma das estações das macrorregiões; os anos mínimo e máximo e o período cobrem todas elas.
4. **No painel, o estado é um nível explícito** (`nivel = 'estado'`, `regiao = 'Espírito Santo'`), escolhido no segmentador como as regiões, e não um comportamento implícito de "nenhuma região selecionada".

## Alternativas consideradas

- **Média simples das estações:** é a mesma regra das regiões, mas a Metropolitana pesaria cerca de 38% do estado e puxaria a média para o litoral.
- **Média das macrorregiões ponderada pela área:** é a mais próxima da chuva que cai sobre o território, mas transmite uma precisão que 13 estações não sustentam. Fica junto das evoluções espaciais previstas na ADR 0004 (preenchimento pelas vizinhas, relevo, produtos de satélite).
- **Estado como resultado de "nenhuma seleção":** é comum em painéis, mas é implícito, porque quem lê vê números sem saber de onde vêm.

## Consequências

- A média estadual é a **média das macrorregiões**, e não a chuva média sobre o território. O painel deve dizer isso no texto de contexto.
- Uma macrorregião com uma ou duas estações pesa um quarto do estado; o número de estações exibido deixa essa fragilidade visível.
- Se uma macrorregião deixar de ter estações válidas num mês, o estado fica sem valor naquele mês, em vez de mudar de composição.
- A view passa a ter 12 linhas a mais (uma por mês), no nível `estado`.
