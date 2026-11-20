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