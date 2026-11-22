-- Validação: o banco reproduz o notebook de exploração da A612 (2021–2025)?
-- Referência: notebooks/01-exploracao-vitoria.ipynb
-- Os meses e anos são agrupados em UTC, como no notebook (coluna 'Data' do CSV).

SET client_encoding = 'UTF8';

-- 1. Horas e horas sem registro de chuva, por ano
SELECT extract(year FROM m.data_hora_utc AT TIME ZONE 'UTC')::int AS ano,
       count(*) AS horas,
       count(*) - count(m.valor) AS sem_registro
FROM f_medicao AS m
JOIN dim_estacao AS e USING (id_estacao)
JOIN dim_variavel AS v USING (id_variavel)
WHERE e.codigo = 'A612'
  AND v.codigo = 'precipitacao'
  AND m.data_hora_utc >= '2021-01-01 00:00+00'
  AND m.data_hora_utc <  '2026-01-01 00:00+00'
GROUP BY ano
ORDER BY ano;


-- 2. Completude mensal da chuva e classificação dos meses (critério do notebook)
--    >= 90%: válido | 75% a 90%: baixa confiança | < 75%: excluído
WITH mensal AS (
    SELECT date_trunc('month', m.data_hora_utc AT TIME ZONE 'UTC') AS mes,
           count(m.valor)::numeric / count(*) AS completude
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    JOIN dim_variavel AS v USING (id_variavel)
    WHERE e.codigo = 'A612'
      AND v.codigo = 'precipitacao'
      AND m.data_hora_utc >= '2021-01-01 00:00+00'
      AND m.data_hora_utc <  '2026-01-01 00:00+00'
    GROUP BY mes
)
SELECT CASE
           WHEN completude < 0.75 THEN 'excluído'
           WHEN completude < 0.90 THEN 'válido, baixa confiança'
           ELSE 'válido'
       END AS classe,
       count(*) AS meses,
       string_agg(to_char(mes, 'MM/YYYY'), ', ' ORDER BY mes) AS quais
FROM mensal
GROUP BY classe
ORDER BY classe;


-- 3. Total anual de chuva, somando só os meses válidos (ranking anual do notebook)
WITH mensal AS (
    SELECT date_trunc('month', m.data_hora_utc AT TIME ZONE 'UTC') AS mes,
           sum(m.valor) AS total_mm,
           count(m.valor)::numeric / count(*) AS completude
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    JOIN dim_variavel AS v USING (id_variavel)
    WHERE e.codigo = 'A612'
      AND v.codigo = 'precipitacao'
      AND m.data_hora_utc >= '2021-01-01 00:00+00'
      AND m.data_hora_utc <  '2026-01-01 00:00+00'
    GROUP BY mes
)
SELECT extract(year FROM mes)::int AS ano,
       round(sum(total_mm), 1) AS total_mm,
       count(*) AS meses_validos
FROM mensal
WHERE completude >= 0.75
GROUP BY ano
ORDER BY total_mm DESC;

-- 4. Média, mínimo e máximo do total mensal de chuva, por mês do calendário (só meses válidos)
WITH mensal AS (
    SELECT date_trunc('month', m.data_hora_utc AT TIME ZONE 'UTC') AS mes,
           sum(m.valor) AS total_mm,
           count(m.valor)::numeric / count(*) AS completude
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    JOIN dim_variavel AS v USING (id_variavel)
    WHERE e.codigo = 'A612'
      AND v.codigo = 'precipitacao'
      AND m.data_hora_utc >= '2021-01-01 00:00+00'
      AND m.data_hora_utc <  '2026-01-01 00:00+00'
    GROUP BY mes
)
SELECT extract(month FROM mes)::int AS mes,
       round(avg(total_mm), 1) AS media_mm,
       round(min(total_mm), 1) AS min_mm,
       round(max(total_mm), 1) AS max_mm,
       count(*) AS n_anos
FROM mensal
WHERE completude >= 0.75
GROUP BY 1
ORDER BY 1;

-- 5. Efeito do fuso: total mensal de chuva agrupado em UTC (como o notebook) e no horário de Vitória
--    Mostra só os meses em que os dois totais diferem.
WITH utc AS (
    SELECT to_char(m.data_hora_utc AT TIME ZONE 'UTC', 'YYYY-MM') AS mes,
           sum(m.valor) AS total_mm
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    JOIN dim_variavel AS v USING (id_variavel)
    WHERE e.codigo = 'A612'
      AND v.codigo = 'precipitacao'
      AND m.data_hora_utc >= '2021-01-01 00:00+00'
      AND m.data_hora_utc <  '2026-01-01 00:00+00'
    GROUP BY mes
),
local AS (
    SELECT to_char(m.data_hora_utc AT TIME ZONE 'America/Sao_Paulo', 'YYYY-MM') AS mes,
           sum(m.valor) AS total_mm
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    JOIN dim_variavel AS v USING (id_variavel)
    WHERE e.codigo = 'A612'
      AND v.codigo = 'precipitacao'
      AND m.data_hora_utc >= '2021-01-01 00:00 America/Sao_Paulo'
      AND m.data_hora_utc <  '2026-01-01 00:00 America/Sao_Paulo'
    GROUP BY mes
)
SELECT mes,
       u.total_mm AS total_utc,
       l.total_mm AS total_local,
       l.total_mm - u.total_mm AS diferenca
FROM utc AS u
JOIN local AS l USING (mes)
WHERE l.total_mm <> u.total_mm
ORDER BY abs(l.total_mm - u.total_mm) DESC;

-- 6. Conferência da carga histórica (#29): nenhuma medição anterior ao início de operação da estação
SELECT e.codigo,
       e.data_inicio_operacao AS inicio_cadastro,
       min(m.data_hora_utc) AT TIME ZONE 'UTC' AS primeira_medicao_utc,
       count(*) FILTER (
           WHERE m.data_hora_utc < e.data_inicio_operacao::timestamp AT TIME ZONE 'UTC'
       ) AS medicoes_antes_do_inicio
FROM f_medicao AS m
JOIN dim_estacao AS e USING (id_estacao)
GROUP BY e.codigo, e.data_inicio_operacao
ORDER BY e.codigo;