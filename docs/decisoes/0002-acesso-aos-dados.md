# 0002 — Acesso aos dados: portal para o histórico, API para os dados recentes

- **Data:** 2026-11-14
- **Status:** aceita
- **Relação:** complementa a [ADR 0001](0001-fonte-de-dados.md); baseada no [levantamento dos canais do INMET](../levantamento-canais-inmet.md) (#10)

## Contexto

A ADR 0001 definiu as estações automáticas do INMET como fonte de dados. Faltava decidir **como** obter esses dados. O levantamento de 13 e 14/11/2026 testou quatro canais:

- **Portal de dados históricos:** histórico completo desde 2000, em ZIPs anuais, mas com download apenas manual (o servidor recusa acesso por script) e atraso de semanas (em 13/11, dados até 31/10);
- **BDMEP:** dados com cerca de 1 h de atraso, mas com fluxo por e-mail, fila e um pedido por vez;
- **Tabela de Dados das Estações (TEMPO):** dados com menos de 1 h de atraso, mas protegida por reCAPTCHA e limitada a 6 meses por consulta;
- **API (apitempo):** único canal previsto para acesso automatizado; sem token, a rota de dados horários retorna HTTP 204, e a documentação oficial está indisponível.

As necessidades do produto são diferentes: as histórias 1 a 3 (comparação com a série histórica, períodos chuvoso e seco, informação para a imprensa) toleram atraso de semanas; a história 4 (últimas 24 h) exige dados horários com atraso de cerca de 1 h e coleta automatizada.

## Decisão

1. **Histórico (histórias 1 a 3):** obtido do portal de dados históricos, por download manual dos ZIPs anuais, com carga única da série e atualizações manuais periódicas.
2. **Dados recentes (história 4):** obtidos da API, com token, por coleta automatizada (robô diário, Etapa 4).
3. **Até a obtenção do token:** as histórias 1 a 3 seguem com o portal; dados recentes, quando necessários, são consultados manualmente na Tabela de Dados das Estações, sem automação.

## Alternativas consideradas

- **Portal para tudo:** descartado para os dados recentes, por causa do atraso de semanas, que não atende à história 4.
- **BDMEP:** dados atualizados, mas o fluxo por e-mail e fila inviabiliza a automação; mantido apenas para pedidos pontuais.
- **Automatizar a Tabela ou o portal contornando as proteções:** descartado. Os dois canais foram protegidos contra acesso automatizado (reCAPTCHA e bloqueio de scripts), e contornar essas proteções contraria o uso previsto pelo INMET.
- **Outras fontes (Cemaden, ANA, satélite):** fora do escopo atual, conforme a ADR 0001.

## Consequências

- A Etapa 4 (robô diário) fica **bloqueada até a obtenção do token**, pedido em 14/11/2026 (#12).
- O ETL precisa ler o formato do portal agora e o da API quando o token chegar; o uso provisório da Tabela introduz um terceiro formato.
- O painel deve informar a data da última atualização dos dados, como já preveem as histórias de usuário.
- Riscos registrados: documentação oficial da API indisponível; token sem prazo; dados brutos, sem validação pelo INMET; atualização manual sujeita a interrupções.
- Esta decisão deve ser revista quando o token for concedido, ou se for negado.