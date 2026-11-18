# Dados de referência

Tabelas pequenas, montadas para o projeto a partir de fontes oficiais. Diferentemente de `data/raw/`, são versionadas.

## regionalizacao_es.csv

Relação dos 78 municípios do ES com a microrregião e a macrorregião de planejamento.

- **Fonte:** Lei Estadual nº 9.768, de 26/12/2011, com o Anexo Único na redação dada pela Lei nº 11.174/2020 (texto consolidado de LeisEstaduais.com.br, gerado em 19/01/2024). Macrorregiões conforme o Art. 6º.
- **Código dos municípios:** `cd_municipio` é o código IBGE, da Malha Municipal 2025.
- **Ajustes feitos ao cruzar a lei com o IBGE:**
  - "Baixo Gandu", grafado assim no Anexo Único, foi associado ao município de **Baixo Guandu** (IBGE 3200805);
  - "Atílio Vivacqua" foi grafado como **Atílio Vivácqua**, como no IBGE (3200706);
  - a lei chama a mesma microrregião de "Central Sul" (Arts. 4º e 6º) e de "Centro Sul" (Anexo Único); adotou-se **Central Sul**, o nome dos artigos.
- **Conferência:** 78 municípios, cada um em uma única microrregião; totais por microrregião iguais aos do mapa de microrregiões de planejamento do Idaf.
