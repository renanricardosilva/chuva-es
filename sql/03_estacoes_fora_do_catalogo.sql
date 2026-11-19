-- Estações automáticas do INMET no ES que não constam no catálogo de 14/11/2026
-- (data/raw/catalogo/), mas têm dados históricos publicados. Provavelmente desativadas;
-- como o status oficial é desconhecido, a situação fica NULL.
-- Valores copiados do cabeçalho do CSV mais recente de cada estação em data/raw/inmet/:
--   A615: arquivo de 2024 (últimos dados em 31/12/2024)
--   A623: arquivo de 2022 (últimos dados em 31/12/2022)
-- Idempotente: se a estação já existe, atualiza os dados.

SET client_encoding = 'UTF8';

INSERT INTO dim_estacao (codigo, nome, id_fonte, situacao, altitude_m, data_inicio_operacao, geom) VALUES
    ('A615', 'ALFREDO CHAVES', (SELECT id_fonte FROM dim_fonte WHERE sigla = 'INMET'), NULL,  14.19, '2006-11-03',
     ST_SetSRID(ST_MakePoint(-40.74194444, -20.63638888), 4674)),
    ('A623', 'NOVA VENECIA',   (SELECT id_fonte FROM dim_fonte WHERE sigla = 'INMET'), NULL, 156.02, '2008-06-22',
     ST_SetSRID(ST_MakePoint(-40.39055555, -18.69527777), 4674))
ON CONFLICT (id_fonte, codigo) DO UPDATE SET
    nome                 = EXCLUDED.nome,
    situacao             = EXCLUDED.situacao,
    altitude_m           = EXCLUDED.altitude_m,
    data_inicio_operacao = EXCLUDED.data_inicio_operacao,
    geom                 = EXCLUDED.geom;