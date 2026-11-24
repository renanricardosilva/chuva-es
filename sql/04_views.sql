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