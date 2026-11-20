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