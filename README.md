# chuva-es

*Pipeline automatizado de dados de chuva do INMET para o Espírito Santo — Python, PostgreSQL/PostGIS, QGIS e Power BI.*

## Por que este projeto

As chuvas no Espírito Santo apresentam regionalidades ao longo do território, variando muito entre litoral, região serrana e norte do estado, mas a rede de monitoramento automáticas do INMET tem apenas 11 estações em solo capixaba. Transformar esses registros em informação por região apoia decisões sobre estiagem, eventos extremos e gestão ambiental — como as que envolvem a SEAMA e sua Gerência de Gestão e Qualidade Ambiental.

## Visão do produto

Um painel de chuva do Espírito Santo com dois públicos:

- **Gestão pública (SEAMA):** dados para embasar decisões, sobretudo sobre mudanças climáticas e episódios críticos de chuva.
- **Sociedade:** informação aberta sobre o histórico de chuvas, para pesquisadores, jornalistas, turistas e a população.

O painel compara o ano atual (ou um ano escolhido) com a série histórica, por localidade, e mostra a chuva hora a hora das últimas 24 horas.

### Histórias de usuário

**1. Comparação com a série histórica**
> **Como** gestor da SEAMA, **quero** comparar a chuva acumulada do ano atual com a média histórica da macrorregião que eu escolher, **para** identificar se a região está mais seca ou mais chuvosa que o normal e embasar decisões sobre estiagem ou eventos extremos.

- [ ] Posso escolher uma macrorregião e um ano
- [ ] Vejo a chuva acumulada mês a mês, ao lado da média do período de referência
- [ ] Vejo, em destaque, quanto o acumulado está acima ou abaixo da média (%)
- [ ] O painel informa até que data os dados vão

**2. Período chuvoso e seco**
> **Como** morador ou turista, **quero** ver em quais meses mais chove na região, **para** planejar atividades no período mais adequado (plantio, obras, viagens).

- [ ] Vejo a chuva média de cada mês do ano, para a região escolhida
- [ ] Os meses mais secos e mais chuvosos aparecem destacados

**3. Informação para a imprensa**
> **Como** jornalista, **quero** saber se a chuva deste ano está acima ou abaixo do normal na região, **para** informar a população com dados oficiais quando houver estiagem ou excesso de chuva.

- [ ] Vejo o acumulado do ano comparado à média histórica, em percentual
- [ ] Vejo a fonte e a data da última atualização dos dados

**4. Acompanhamento das últimas 24 horas**
> **Como** gestor da SEAMA, **quero** ver a chuva hora a hora das últimas 24 horas nas estações do ES, **para** subsidiar a articulação da resposta do Estado, junto à Defesa Civil, em episódios de chuva intensa que possam evoluir para situações de emergência ou calamidade.

- [ ] Posso escolher uma estação e ver a chuva de cada hora das últimas 24 h, com o total acumulado
- [ ] O painel mostra o horário da última atualização
- [ ] O painel informa que os dados são de acompanhamento e não substituem os alertas oficiais da Defesa Civil e do Cemaden

### Limites declarados

- A rede de estações automáticas do INMET no ES é esparsa (11 estações), por isso chuvas muito localizadas podem não ser registradas.
- Com cerca de 18 anos de dados automáticos, o painel mostra **variabilidade**, mas não permite afirmar **tendências climáticas**, que exigem séries de 30 anos ou mais.

## O que o projeto entrega

- **Robô diário** que verifica diariamente se o INMET publicou dados novos e os processa
- **Banco de dados** PostgreSQL/PostGIS com estações, municípios e regiões
- **Mapas no QGIS** do estado e distribuição da chuva
- **Painel no Power BI** com análises por regionalizadas

## Fonte dos dados

- [INMET — dados históricos das estações automáticas](https://portal.inmet.gov.br/dadoshistoricos)
- Bases oficiais do Governo do Espírito Santo (regionalização, limites municipais ou outras informações que se mostrarem pertinentes)

## Roteiro

- [x] Etapa 0 — Fundação: repositório, documentação e sonda do INMET
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