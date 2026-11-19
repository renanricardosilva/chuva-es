"""Carga das medições horárias do INMET na tabela f_medicao (formato longo)."""
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import text
from etl.db import get_engine
from etl.inmet import read_inmet, read_station_code, to_long

SELECT_STATION = text("""
    SELECT e.id_estacao
    FROM dim_estacao AS e
    JOIN dim_fonte AS f USING (id_fonte)
    WHERE f.sigla = 'INMET' AND e.codigo = :codigo;
""")

SELECT_VARIABLES = text("SELECT codigo, id_variavel FROM dim_variavel;")

UPSERT_MEASUREMENT = text("""
    INSERT INTO f_medicao (id_estacao, id_variavel, data_hora_utc, valor)
    VALUES (:id_estacao, :id_variavel, :data_hora_utc, :valor)
    ON CONFLICT (id_estacao, id_variavel, data_hora_utc)
    DO UPDATE SET valor = EXCLUDED.valor;
""")


def load_file(conn, path, variable_ids):
    """Carrega um arquivo do INMET na f_medicao e devolve o número de linhas gravadas."""
    code = read_station_code(path)
    station_id = conn.execute(SELECT_STATION, {'codigo': code}).scalar_one_or_none()
    if station_id is None:
        raise ValueError(f'Estação {code} não cadastrada em dim_estacao: {path}')

    df = to_long(read_inmet(path))
    rows = [
        {
            'id_estacao': station_id,
            'id_variavel': variable_ids[row.variavel],
            'data_hora_utc': row.data_hora_utc.to_pydatetime(),
            'valor': None if pd.isna(row.valor) else float(row.valor),
        }
        for row in df.itertuples(index=False)
    ]
    conn.execute(UPSERT_MEASUREMENT, rows)
    return len(rows)


def main():
    path = Path(sys.argv[1])
    engine = get_engine()
    with engine.begin() as conn:
        variable_ids = dict(conn.execute(SELECT_VARIABLES).all())
        count = load_file(conn, path, variable_ids)
    print(f'{path.name}: {count} linhas gravadas')


if __name__ == '__main__':
    main()