-- 04_views.sql
-- Views para o consumo dos dados (Power BI e análises), conforme a ADR 0004.
-- Idempotente: CREATE OR REPLACE recria as views com a definição atual.

SET client_encoding = 'UTF8';

-- Chuva mensal por estação, no horário de Vitória
CREATE OR REPLACE VIEW vw_chuva_mensal_estacao AS
WITH mensal AS (
    SELECT m.id_estacao,
           date_trunc('month', m.data_hora_utc AT TIME ZONE 'America/Sao_Paulo')::date AS mes,
           sum(m.valor)   AS total_mm,
           count(m.valor) AS horas_com_registro
    FROM f_medicao AS m
    JOIN dim_variavel AS v USING (id_variavel)
    WHERE v.codigo = 'precipitacao'
    GROUP BY m.id_estacao, mes
),
com_horas_do_mes AS (
    SELECT mensal.*,
           (extract(epoch FROM ((mes::timestamp + interval '1 month') AT TIME ZONE 'America/Sao_Paulo')
                             - (mes::timestamp AT TIME ZONE 'America/Sao_Paulo')) / 3600)::int AS horas_do_mes
    FROM mensal
),
com_completude AS (
    SELECT com_horas_do_mes.*,
           horas_com_registro::numeric / horas_do_mes AS completude
    FROM com_horas_do_mes
)
SELECT id_estacao, mes, total_mm, horas_com_registro, horas_do_mes, completude,
       CASE
           WHEN completude < 0.75 THEN 'excluído'
           WHEN completude < 0.90 THEN 'válido, baixa confiança'
           ELSE 'válido'
       END AS classe
FROM com_completude;

COMMENT ON VIEW vw_chuva_mensal_estacao IS
    'Chuva mensal por estação, no horário de Vitória (ADR 0004): total, horas com registro, horas do mês pelo calendário (considera o horário de verão), completude e classe (válido >= 90%; baixa confiança de 75% a 90%; excluído < 75%).';


-- Climatologia mensal por estação: média dos meses válidos, com mínimo de 5 anos (ADR 0004)
CREATE OR REPLACE VIEW vw_climatologia_mensal_estacao AS
SELECT id_estacao,
       extract(month FROM mes)::int AS mes_do_ano,
       avg(total_mm)                AS chuva_media_mm,
       count(*)                     AS n_anos,
       min(extract(year FROM mes))::int AS ano_inicio,
       max(extract(year FROM mes))::int AS ano_fim
FROM vw_chuva_mensal_estacao
WHERE classe <> 'excluído'
GROUP BY id_estacao, mes_do_ano
HAVING count(*) >= 5;

COMMENT ON VIEW vw_climatologia_mensal_estacao IS
    'Chuva média de cada mês do ano, por estação, com os meses válidos (inclusive os de baixa confiança). Só entram estações com pelo menos 5 anos válidos naquele mês (ADR 0004).';

-- Climatologia mensal por região: média simples entre as estações da região (ADR 0004)
CREATE OR REPLACE VIEW vw_climatologia_mensal_regiao AS
WITH estacao_regiao AS (
    SELECT c.*,
           mi.nome AS microrregiao,
           ma.nome AS macrorregiao
    FROM vw_climatologia_mensal_estacao AS c
    JOIN dim_estacao      AS e  USING (id_estacao)
    JOIN dim_municipio    AS mu USING (id_municipio)
    JOIN dim_microrregiao AS mi USING (id_microrregiao)
    JOIN dim_macrorregiao AS ma USING (id_macrorregiao)
)
SELECT 'macrorregião' AS nivel, macrorregiao AS regiao, mes_do_ano,
       avg(chuva_media_mm) AS chuva_media_mm,
       count(*)    AS n_estacoes,
       min(n_anos) AS n_anos_min,
       max(n_anos) AS n_anos_max
FROM estacao_regiao
GROUP BY macrorregiao, mes_do_ano
UNION ALL
SELECT 'microrregião', microrregiao, mes_do_ano,
       avg(chuva_media_mm), count(*), min(n_anos), max(n_anos)
FROM estacao_regiao
GROUP BY microrregiao, mes_do_ano;

COMMENT ON VIEW vw_climatologia_mensal_regiao IS
    'Chuva média de cada mês do ano por macro e microrregião: média simples das climatologias das estações da região (ADR 0004), com o número de estações e o mínimo e o máximo de anos usados.';