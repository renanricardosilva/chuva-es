# chuva-es

*Pipeline automatizado de dados de chuva do INMET para o Espírito Santo — Python, PostgreSQL/PostGIS, QGIS e Power BI.*

## Por que este projeto

As chuvas no Espírito Santo apresentam regionalidades ao longo do território, variando muito entre litoral, região serrana e norte do estado, mas a rede de monitoramento automáticas do INMET tem apenas 11 estações em solo capixaba. Transformar esses registros em informação por região apoia decisões sobre estiagem, eventos extremos e gestão ambiental — como as que envolvem a SEAMA e sua Gerência de Gestão e Qualidade Ambiental.

## O que o projeto entrega

- **Robô diário** que verifica diariamente se o INMET publicou dados novos e os processa
- **Banco de dados** PostgreSQL/PostGIS com estações, municípios e regiões
- **Mapas no QGIS** do estado e distribuição da chuva
- **Painel no Power BI** com análises por regionalizadas

## Fonte dos dados

- [INMET — dados históricos das estações automáticas](https://portal.inmet.gov.br/dadoshistoricos)
- Bases oficiais do Governo do Espírito Santo (regionalização, limites municipais ou outras informações que se mostrarem pertinentes)

## Roteiro

- [ ] Etapa 0 — Fundação: repositório, documentação e sonda do INMET
- [ ] Etapa 1 — Entendimento dos dados
- [ ] Etapa 2 — Extração e transformação (ETL)
- [ ] Etapa 3 — Robô diário de verificação e atualização
- [ ] Etapa 4 — Modelagem e banco de dados
- [ ] Etapa 5 — Mapas no QGIS
- [ ] Etapa 6 — Do QGIS ao código (PostGIS)
- [ ] Etapa 7 — Painel no Power BI
- [ ] Etapa 8 — Validação e aplicação

## Status

🚧 Em construção — Etapa 0.