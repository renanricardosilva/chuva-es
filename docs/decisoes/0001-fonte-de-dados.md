# 0001 — Fonte de dados: estações automáticas do INMET

- **Data:** 2026-11-09
- **Status:** aceita

## Contexto

O Instituto Nacional de Meteorologia - INMET fornece dados públicos oficiais de chuvas do território nacional, em arquivos anuais, com o ano vigente sendo reescrito mensalmente. Os dados são capturados em estações automáticas com dados horários.

Dados do Espírito Santo constam a partir de 2006, com cobertura razoável a partir de 2008, sendo atualmente fornecidos por onze estações, podendo ser capturados em pasta zipada, identificando os arquivos de interesse através da seguinte estrutura:

INMET_SE_ES_[restante_do_nome_do_arquivo]

## Decisão

Usar os dados horários das estações automáticas do INMET como fonte principal de chuva do projeto, obtidos dos arquivos anuais publicados no portal de dados históricos.

## Alternativas consideradas

Dados de bases estaduais, como os dados do Incaper ou outros podem ser considerados. Também poderá ser incorporados dados oriundos de monitoramento satelital.

No contexto nacional, dados da ANA (Hidroweb) e do Cemaden, ou mesmo do CHIRPS serão avaliados.

A escolha apenas dos dados do INMET e o não uso de nenhuma dessas outras alternativas se dá pela praticidade de aquisição pela instituição, sendo a referência nacional sobre meteorologia e, principalmente, para começar pequeno, validar modelo e, com uma estrutura pronta e rodando, poder escalar para outras frentes.

## Consequências

Com a utilização de dados públicos não haverá custo de aquisição do dado.

Ganhos identificados: dado oficial, padronizado, com resolução horária e uma série histórica de quase 20 anos.

Defasagem de até um mês entre a ocorrência e a publicação: os dados servem para análise e planejamento, não para alerta em tempo real.

Também há limitação geográfica, pois há apenas onze estações para um estado com 78 municípios, com espaços vazios de cobertura do monitoramento.