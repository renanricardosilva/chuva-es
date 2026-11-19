"""Leitura dos arquivos CSV de dados horários das estações automáticas do INMET."""
import pandas as pd

ENCODING = 'latin-1'
METADATA_LINES = 8  # linhas de cabeçalho antes da tabela (região, UF, estação, código...)


def read_station_code(path):
    """Lê o código da estação (ex.: 'A612') nas linhas de cabeçalho do arquivo."""
    with open(path, encoding=ENCODING) as file:
        for _ in range(METADATA_LINES):
            key, value = file.readline().split(';')[:2]
            if key.startswith('CODIGO'):
                return value.strip()
    raise ValueError(f'Código da estação não encontrado no cabeçalho de {path}')


def read_inmet(path):
    """Lê os dados horários de um CSV do INMET no formato usado a partir de 2019.

    Acrescenta a coluna 'data_hora_utc' (timestamp com fuso UTC), juntando 'Data' e 'Hora UTC'.
    """
    df = pd.read_csv(path, encoding=ENCODING, skiprows=METADATA_LINES, decimal=',', sep=';')
    if 'Hora UTC' not in df.columns:
        raise ValueError(f'Formato anterior a 2019 ainda não suportado (ver issue #29): {path}')
    df = df.drop(columns=[c for c in df.columns if c.startswith('Unnamed')])
    df['data_hora_utc'] = pd.to_datetime(
        df['Data'] + ' ' + df['Hora UTC'], format='%Y/%m/%d %H%M UTC', utc=True
    )
    return df