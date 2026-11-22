"""Carga das medições horárias do INMET na tabela f_medicao (formato longo)."""
import sys
from pathlib import Path
import pandas as pd
import time
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

INMET_DIR = Path('data/raw/inmet')

SUMMARY = text("""
    SELECT e.codigo, e.nome,
           extract(year FROM m.data_hora_utc AT TIME ZONE 'UTC')::int AS ano,
           count(*) FILTER (WHERE v.codigo = 'precipitacao') AS horas,
           count(*) FILTER (WHERE v.codigo = 'precipitacao' AND m.valor IS NULL) AS sem_chuva,
           count(*) FILTER (WHERE v.codigo = 'temperatura_ar' AND m.valor IS NULL) AS sem_temperatura
    FROM f_medicao AS m
    JOIN dim_estacao AS e USING (id_estacao)
    JOIN dim_variavel AS v USING (id_variavel)
    GROUP BY e.codigo, e.nome, ano
    ORDER BY e.codigo, ano;
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

    engine = get_engine()
    start = time.perf_counter()
    with engine.connect() as conn:
        variable_ids = dict(conn.execute(SELECT_VARIABLES).all())

    total = 0
    for i, path in enumerate(paths, start=1):
        with engine.begin() as conn:  # uma transação por arquivo
            count = load_file(conn, path, variable_ids)
        total += count
        print(f'[{i}/{len(paths)}] {path.name}: {count} linhas')

    elapsed = time.perf_counter() - start
    print(f'\nArquivos carregados: {len(paths)}')
    print(f'Linhas gravadas nesta execução: {total} | tempo: {elapsed:.0f} s\n')

    with engine.connect() as conn:
        summary = conn.execute(SUMMARY).all()
    print('Situação da f_medicao por estação e ano (horas sem registro):')
    current = None
    for codigo, nome, ano, horas, sem_chuva, sem_temperatura in summary:
        if codigo != current:
            print(f'\n  {codigo} {nome}')
            current = codigo
        print(f'    {ano}: {horas:>5} h | sem chuva: {sem_chuva:>5} | sem temperatura: {sem_temperatura:>5}')


if __name__ == '__main__':
    main()