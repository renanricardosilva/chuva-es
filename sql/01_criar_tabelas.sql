-- 01_criar_tabelas.sql
-- Cria as tabelas do banco ambiental_es, conforme a ADR 0003 (docs/modelo-dados.md).
-- Pode ser executado mais de uma vez: só cria o que ainda não existe.
-- O arquivo está em UTF-8; sem esta linha, o psql do Windows o leria como WIN1252
SET client_encoding = 'UTF8';

-- Fontes dos dados (INMET, IBGE, IJSN...)
CREATE TABLE IF NOT EXISTS dim_fonte (
    id_fonte  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sigla     text NOT NULL UNIQUE,
    nome      text NOT NULL,
    url       text
);
COMMENT ON TABLE dim_fonte IS 'Instituições que fornecem os dados (ex.: INMET, IBGE).';

-- Variáveis medidas (precipitação, temperatura...)
CREATE TABLE IF NOT EXISTS dim_variavel (
    id_variavel  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo       text NOT NULL UNIQUE,
    nome         text NOT NULL,
    unidade      text NOT NULL,
    agregacao    text NOT NULL CHECK (agregacao IN ('soma', 'media'))
);
COMMENT ON TABLE dim_variavel IS 'Variáveis medidas, com unidade e forma de agregação (soma ou média).';

-- Regionalização do ES: macrorregiões de planejamento
CREATE TABLE IF NOT EXISTS dim_macrorregiao (
    id_macrorregiao  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome             text NOT NULL UNIQUE
);
COMMENT ON TABLE dim_macrorregiao IS 'Macrorregiões de planejamento do Espírito Santo.';

-- Regionalização do ES: microrregiões, cada uma dentro de uma macrorregião
CREATE TABLE IF NOT EXISTS dim_microrregiao (
    id_microrregiao  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome             text NOT NULL UNIQUE,
    id_macrorregiao  smallint NOT NULL REFERENCES dim_macrorregiao (id_macrorregiao)
);
COMMENT ON TABLE dim_microrregiao IS 'Microrregiões de planejamento do Espírito Santo.';

-- Municípios do ES, com o limite territorial
CREATE TABLE IF NOT EXISTS dim_municipio (
    id_municipio     integer PRIMARY KEY,
    nome             text NOT NULL,
    id_microrregiao  smallint NOT NULL REFERENCES dim_microrregiao (id_microrregiao),
    geom             geometry(MultiPolygon, 4674) NOT NULL
);
COMMENT ON TABLE dim_municipio IS 'Municípios do ES; id_municipio é o código IBGE de 7 dígitos.';
CREATE INDEX IF NOT EXISTS idx_municipio_geom ON dim_municipio USING gist (geom);

-- Estações (pontos de monitoramento), de qualquer fonte
CREATE TABLE IF NOT EXISTS dim_estacao (
    id_estacao            integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo                text NOT NULL,
    nome                  text NOT NULL,
    id_fonte              smallint NOT NULL REFERENCES dim_fonte (id_fonte),
    id_municipio          integer REFERENCES dim_municipio (id_municipio),
    situacao              text,
    altitude_m            numeric(7, 2),
    data_inicio_operacao  date,
    geom                  geometry(Point, 4674) NOT NULL,
    UNIQUE (id_fonte, codigo)
);
COMMENT ON TABLE dim_estacao IS 'Pontos de monitoramento; o código é único dentro de cada fonte.';
CREATE INDEX IF NOT EXISTS idx_estacao_geom ON dim_estacao USING gist (geom);

-- Medições: uma linha por estação, variável e momento (formato longo)
CREATE TABLE IF NOT EXISTS f_medicao (
    id_estacao     integer     NOT NULL REFERENCES dim_estacao (id_estacao),
    id_variavel    smallint    NOT NULL REFERENCES dim_variavel (id_variavel),
    data_hora_utc  timestamptz NOT NULL,
    valor          numeric,
    PRIMARY KEY (id_estacao, id_variavel, data_hora_utc)
);
COMMENT ON TABLE f_medicao IS 'Medições horárias em UTC; valor nulo indica hora sem registro.';