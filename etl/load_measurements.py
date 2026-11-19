"""Carga das medições horárias do INMET na tabela f_medicao (formato longo)."""
import sys
from pathlib import Path
import pandas as pd
import time
from sqlalchemy import text
from etl.db import get_engine
from etl.inmet import is_current_format, read_inmet, read_station_code, to_long

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

INMET_DIR = Path('data/raw/inmet')

SUMMARY = text("""
    SELECT e.codigo, e.nome,
           count(*) AS linhas,
           count(*) - count(m.valor) AS nulos,
           (min(m.data_hora_utc) AT TIME ZONE 'UTC')::date AS inicio,
           (max(m.data_hora_utc) AT TIME ZONE 'UTC')::date AS fim
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    GROUP BY e.codigo, e.nome
    ORDER BY e.codigo;
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
    """Carrega os arquivos indicados na linha de comando ou, se nenhum for indicado, todos de data/raw/inmet."""
    paths = [Path(arg) for arg in sys.argv[1:]] or sorted(INMET_DIR.glob('*.CSV'))
    supported = [path for path in paths if is_current_format(path)]
    skipped = len(paths) - len(supported)

    engine = get_engine()
    start = time.perf_counter()
    with engine.connect() as conn:
        variable_ids = dict(conn.execute(SELECT_VARIABLES).all())

    total = 0
    for i, path in enumerate(supported, start=1):
        with engine.begin() as conn:  # uma transação por arquivo
            count = load_file(conn, path, variable_ids)
        total += count
        print(f'[{i}/{len(supported)}] {path.name}: {count} linhas')

    elapsed = time.perf_counter() - start
    print(f'\nArquivos carregados: {len(supported)} | ignorados (formato anterior a 2019, ver #29): {skipped}')
    print(f'Linhas gravadas nesta execução: {total} | tempo: {elapsed:.0f} s\n')

    with engine.connect() as conn:
        summary = conn.execute(SUMMARY).all()
    print('Situação da f_medicao por estação:')
    for codigo, nome, linhas, nulos, inicio, fim in summary:
        print(f'  {codigo} {nome:<25} {linhas:>7} linhas | {nulos:>6} nulos | {inicio} a {fim}')


if __name__ == '__main__':
    main()