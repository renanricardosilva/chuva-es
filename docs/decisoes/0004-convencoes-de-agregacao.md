# 0004 — Convenções de agregação das medições

- **Data:** 2026-11-22
- **Status:** aceita
- **Relação:** complementa a [ADR 0003](0003-modelo-de-dados.md); baseada nos achados da [validação do banco](../validacao-a612.md); implementada nas views de `sql/04_views.sql` (#30)

## Contexto

O banco guarda medições **horárias**, em **UTC**, por **estação** (ADR 0003). O painel precisa de outra escala: totais e médias por dia, mês e ano, e por **região** (micro e macrorregião). As regras dessa passagem estavam espalhadas (notebook, validação, decisões em conversa) ou ainda não tinham sido tomadas.

Três achados anteriores pesam na decisão:

- **Fuso:** a validação (#27) mostrou que agrupar os meses em UTC, como fazia o notebook, muda o total de 18 dos 60 meses da A612 (até ±11,8 mm), porque a chuva das 21h à meia-noite do horário local cai no dia seguinte em UTC.
- **Falhas frequentes e de naturezas diferentes:** há anos com falhas em quase toda a rede (2020), falhas só do pluviômetro (A615 em 2021) e falhas crônicas (A631 desde 2024). Como a ausência é gravada como nulo e a soma ignora os nulos, **um período incompleto parece mais seco do que foi**.
- **Rede esparsa e heterogênea:** 13 estações para cerca de 46 mil km², distribuídas de forma desigual entre as regiões, que também têm tamanhos diferentes. A Metropolitana tem estações a cerca de 10 km umas das outras; o Norte é grande e tem poucas.

## Decisão

1. **Fuso:** toda agregação temporal usa o **horário de Vitória** (`America/Sao_Paulo`). O UTC é só a forma de guardar o dado. As consultas de `sql/validacao.sql` continuam em UTC de propósito, porque reproduzem o notebook.
2. **Dia:** **calendário civil**, da meia-noite às 23h59 do horário local.
3. **Variável:** a agregação segue a coluna `agregacao` da `dim_variavel`: **soma** para a precipitação e **média** para a temperatura do ar.
4. **Completude do mês**, por estação e **por variável** (as falhas podem atingir só um sensor): fração das horas do mês com registro.
   - ≥ 90%: **válido**;
   - de 75% a 90%: **válido, baixa confiança** (sinalizado);
   - < 75%: **excluído**.

   O critério é aplicado aos valores exatos, sem arredondamento, como no notebook de exploração.
5. **Ano:** o total anual é a soma dos meses válidos. O ano é **completo** só com os 12 meses válidos; com menos, o valor aparece **sinalizado** como incompleto, com o número de meses válidos, e deve ser lido como um valor mínimo.
6. **Climatologia mensal da estação** (a chuva média de cada mês do calendário): média dos totais dos meses válidos daquele mês. A estação só entra na climatologia de um mês se tiver **pelo menos 5 anos válidos** daquele mês.
7. **Climatologia regional** (micro e macrorregião), em **duas etapas**:
   1. calcula-se a climatologia de cada estação (item 6);
   2. a climatologia da região é a **média simples** das climatologias das estações da região que atingiram o mínimo de anos.

   Cada estação pertence à região do município em que está (consulta espacial da #25). Com as duas etapas, a falha de uma estação num ano reduz o número de anos dela, mas **não muda quais estações compõem a média** daquele mês.
8. **Transparência:** todo valor agregado vem acompanhado do que o sustenta: número de **anos** e de **estações** usados e, quando couber, a completude. O painel mostra essas informações.

## Alternativas consideradas

- **Agrupar em UTC**, como no notebook: descartado, porque desloca para o dia e o mês seguintes a chuva do começo da noite (achado da #27).
- **Dia pluviométrico** (das 9h às 9h do horário local, ou de 12 a 12 UTC), convenção das leituras de pluviômetros convencionais e de boa parte da literatura técnica: dá comparabilidade com redes manuais, mas é menos intuitivo para o público e para cruzamentos com dados administrativos, que usam o dia civil. Como o dado horário está guardado, essa agregação pode ser produzida depois, se for necessária.
- **Critério de completude único e mais rígido** (só ≥ 90%): excluiria muitos meses numa rede com falhas frequentes. A faixa de baixa confiança preserva os dados e deixa a incerteza visível.
- **Mínimo de 10 anos por estação na climatologia:** mais robusto, mas, antes da série histórica completa (#29), excluiria quase todas as estações. Fica para reavaliação com a série de 2006 a 2026.
- **Média regional direta, mês a mês** (média das estações com dado em cada mês): a composição da média muda quando uma estação falha, o que puxa o valor da região para as estações que funcionaram naquele mês.
- **Preenchimento de falhas e ponderação espacial** (inverso da distância, polígonos de Thiessen, krigagem): o inverso da distância foi proposto e é adequado em parte da rede. Foi adiado porque a rede é esparsa, a distância não considera o relevo e os valores estimados exigiriam validação cruzada e sinalização. É candidato para a história de usuário 1, que compara anos específicos e precisa de cada mês, e não só das médias.
- **Um método diferente por região**, conforme a densidade da rede e o tamanho da região: a heterogeneidade é real, mas regiões calculadas de formas diferentes deixariam de ser comparáveis entre si no painel. No MVP, adota-se um método único, com indicadores de qualidade por região.

## Consequências

- As views da #30 implementam estas regras; o Power BI consome números já agregados, sem refazer as regras em DAX.
- Os números do painel diferem dos do notebook de exploração (que usa meses em UTC). A diferença está explicada em `docs/validacao-a612.md`.
- Regiões com poucas estações terão climatologias que dependem de uma ou duas delas; o número de estações exibido deixa isso claro.
- Antes da carga da série histórica (#29), com dados só de 2019 a out/2026, algumas estações podem não alcançar os 5 anos válidos em certos meses e ficar de fora temporariamente da climatologia.
- **Evoluções previstas:**
  - preenchimento de falhas pelas estações vizinhas, com validação cruzada (história 1);
  - métodos regionais adaptados à densidade da rede, com a comparabilidade discutida;
  - consideração do relevo;
  - produtos que combinam satélite e estações (por exemplo, o MERGE, do CPTEC/INPE) para uma estimativa contínua da chuva no território;
  - critério de completude diária, quando houver uso para totais diários (como o acompanhamento das últimas 24 horas);
  - reavaliação do mínimo de 5 para 10 anos com a série completa.
