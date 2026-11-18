"""Carga dos municípios do ES e da regionalização oficial, e ligação de cada estação ao seu município."""
from pathlib import Path
import geopandas as gpd
import pandas as pd
from sqlalchemy import text
from etl.db import get_engine

MALHA = Path('data/raw/ibge/ES_Municipios_2025.shp')
REGIONALIZACAO = Path('data/reference/regionalizacao_es.csv')

UPSERT_MACRO = text("""
    INSERT INTO dim_macrorregiao (nome) VALUES (:macrorregiao)
    ON CONFLICT (nome) DO NOTHING;
""")

UPSERT_MICRO = text("""
    INSERT INTO dim_microrregiao (nome, id_macrorregiao)
    VALUES (:microrregiao,
            (SELECT id_macrorregiao FROM dim_macrorregiao WHERE nome = :macrorregiao))
    ON CONFLICT (nome) DO UPDATE SET id_macrorregiao = EXCLUDED.id_macrorregiao;
""")

UPSERT_MUNICIPIO = text("""
    INSERT INTO dim_municipio (id_municipio, nome, id_microrregiao, geom)
    VALUES (:id_municipio, :nome,
            (SELECT id_microrregiao FROM dim_microrregiao WHERE nome = :microrregiao),
            ST_Multi(ST_GeomFromText(:wkt, 4674)))
    ON CONFLICT (id_municipio) DO UPDATE SET
        nome = EXCLUDED.nome,
        id_microrregiao = EXCLUDED.id_microrregiao,
        geom = EXCLUDED.geom;
""")

LINK_STATIONS = text("""
    UPDATE dim_estacao AS e
    SET id_municipio = m.id_municipio
    FROM dim_municipio AS m
    WHERE ST_Within(e.geom, m.geom);
""")


def read_municipalities():
    """Lê a malha do IBGE e junta a regionalização pelo código do município."""
    malha = gpd.read_file(MALHA)
    if malha.crs.to_epsg() != 4674:
        raise ValueError(f'Sistema de referência inesperado: {malha.crs}')

    regions = pd.read_csv(REGIONALIZACAO, dtype={'cd_municipio': str})
    merged = malha.merge(regions, left_on='CD_MUN', right_on='cd_municipio',
                         how='left', validate='one_to_one')

    missing = merged.loc[merged['microrregiao'].isna(), 'NM_MUN'].tolist()
    if missing or len(regions) != len(malha):
        raise ValueError(f'Malha e regionalização não batem. Sem região: {missing}')
    return merged


def main():
    municipalities = read_municipalities()
    regions = municipalities[['microrregiao', 'macrorregiao']].drop_duplicates()
    rows = [
        {'id_municipio': int(m.CD_MUN), 'nome': m.NM_MUN,
         'microrregiao': m.microrregiao, 'wkt': m.geometry.wkt}
        for m in municipalities.itertuples()
    ]

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(UPSERT_MACRO, regions[['macrorregiao']].drop_duplicates().to_dict('records'))
        conn.execute(UPSERT_MICRO, regions.to_dict('records'))
        conn.execute(UPSERT_MUNICIPIO, rows)
        conn.execute(LINK_STATIONS)

        counts = conn.execute(text("""
            SELECT (SELECT count(*) FROM dim_macrorregiao),
                   (SELECT count(*) FROM dim_microrregiao),
                   (SELECT count(*) FROM dim_municipio),
                   (SELECT count(id_municipio) FROM dim_estacao),
                   (SELECT count(*) FROM dim_estacao);
        """)).one()
        stations = conn.execute(text("""
            SELECT e.codigo, e.nome, m.nome
            FROM dim_estacao AS e LEFT JOIN dim_municipio AS m USING (id_municipio)
            ORDER BY e.codigo;
        """)).all()

    macro, micro, munic, linked, total = counts
    print(f'Macrorregiões: {macro} | Microrregiões: {micro} | Municípios: {munic}')
    print(f'Estações ligadas a um município: {linked} de {total}')
    for codigo, estacao, municipio in stations:
        print(f'  {codigo} {estacao:<25} -> {municipio}')


if __name__ == '__main__':
    main()