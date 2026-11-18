# Dados de referência

Tabelas pequenas, montadas para o projeto a partir de fontes oficiais. Diferentemente de `data/raw/`, são versionadas.

## regionalizacao_es.csv

Relação dos 78 municípios do ES com a microrregião e a macrorregião de planejamento.

- **Fonte:** Lei Estadual nº 9.768, de 26/12/2011, com o Anexo Único na redação dada pela Lei nº 11.174/2020 (texto consolidado de LeisEstaduais.com.br, gerado em 19/01/2024; obtido em 18/11/2026). Macrorregiões conforme o Art. 6º.
- **Código dos municípios:** `cd_municipio` é o código IBGE, da Malha Municipal 2025.
- **Ajustes feitos ao cruzar a lei com o IBGE:**
  - "Baixo Gandu", grafado assim no Anexo Único, foi associado ao município de **Baixo Guandu** (IBGE 3200805);
  - "Atílio Vivacqua" foi grafado como **Atílio Vivácqua**, como no IBGE (3200706);
  - a lei chama a mesma microrregião de "Central Sul" (Arts. 4º e 6º) e de "Centro Sul" (Anexo Único); adotou-se **Central Sul**, o nome dos artigos.
- **Conferência:** 78 municípios, cada um em uma única microrregião; totais por microrregião iguais aos do mapa de microrregiões de planejamento do Idaf.

## Malha municipal do IBGE (não versionada)

As geometrias dos municípios vêm de `data/raw/ibge/ES_Municipios_2025.shp`, lido por `etl/load_municipalities.py`. Por ser dado bruto, o arquivo não fica no repositório. Para reproduzir a carga:

- **Fonte:** IBGE, Malhas Territoriais, **Malha Municipal 2025**, recorte por UF (ES), formato shapefile.
- **Página de download:** <https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html>
- **Obtido em:** 18/11/2026.
- **Sistema de referência:** SIRGAS 2000 (EPSG:4674). A malha é compatível com a escala 1:250.000, o que admite erro de posição das divisas da ordem de 125 m.
- **Onde salvar:** extrair os arquivos (`.shp`, `.shx`, `.dbf`, `.prj`, `.cpg`) em `data/raw/ibge/`. São 78 feições.
- **Caso conhecido:** a estação A613 ("SANTA TERESA") fica a 21 m da divisa e cai em Santa Leopoldina pela consulta espacial. Como a distância é menor que a precisão da malha, mantém-se o resultado do `ST_Within`, sem correção manual. Ver o PR do #25.
