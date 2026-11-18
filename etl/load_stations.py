"""Carga das estações automáticas do INMET no ES (tabela dim_estacao)."""
import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

from etl.db import get_engine

CATALOG = Path('data/raw/catalogo/estacoes_automaticas_2026-11-14.json')
STATE = 'ES'

INSERT_SOURCE = text("""
    INSERT INTO dim_fonte (sigla, nome, url)
    VALUES ('INMET', 'Instituto Nacional de Meteorologia', 'https://portal.inmet.gov.br')
    ON CONFLICT (sigla) DO NOTHING;
""")

UPSERT_STATION = text("""
    INSERT INTO dim_estacao (codigo, nome, id_fonte, situacao, altitude_m,
                             data_inicio_operacao, geom)
    VALUES (:codigo, :nome,
            (SELECT id_fonte FROM dim_fonte WHERE sigla = 'INMET'),
            :situacao, :altitude_m, :data_inicio_operacao,
            ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4674))
    ON CONFLICT (id_fonte, codigo) DO UPDATE SET
        nome = EXCLUDED.nome,
        situacao = EXCLUDED.situacao,
        altitude_m = EXCLUDED.altitude_m,
        data_inicio_operacao = EXCLUDED.data_inicio_operacao,
        geom = EXCLUDED.geom;
""")


def read_stations(path, state):
    """Lê o catálogo de estações do INMET e devolve as do estado indicado."""
    with open(path, encoding='utf-8') as f:
        catalog = json.load(f)

    stations = []
    for item in catalog:
        if item['SG_ESTADO'] != state:
            continue
        start = datetime.fromisoformat(item['DT_INICIO_OPERACAO']).astimezone(timezone.utc)
        stations.append({
            'codigo': item['CD_ESTACAO'],
            'nome': item['DC_NOME'],
            'situacao': item['CD_SITUACAO'],
            'altitude_m': float(item['VL_ALTITUDE']),
            'data_inicio_operacao': start.date(),
            'latitude': float(item['VL_LATITUDE']),
            'longitude': float(item['VL_LONGITUDE']),
        })
    return stations


def main():
    stations = read_stations(CATALOG, STATE)
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(INSERT_SOURCE)
        conn.execute(UPSERT_STATION, stations)
        summary = conn.execute(text(
            'SELECT situacao, count(*) FROM dim_estacao GROUP BY situacao ORDER BY situacao;'
        )).all()

    print(f'Estações do {STATE} lidas do catálogo: {len(stations)}')
    for situacao, total in summary:
        print(f'  {situacao}: {total}')


if __name__ == '__main__':
    main()