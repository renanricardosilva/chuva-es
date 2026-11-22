"""Leitura dos arquivos CSV de dados horários das estações automáticas do INMET."""
import pandas as pd

ENCODING = 'latin-1'
METADATA_LINES = 8  # linhas de cabeçalho antes da tabela (região, UF, estação, código...)
MISSING_VALUE = -9999  # código de dado ausente nos arquivos até 2018

# Colunas do INMET carregadas no banco → código da variável em dim_variavel
VARIABLES = {
    'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'precipitacao',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'temperatura_ar',
}

# Formatos dos CSVs do INMET: colunas de data e hora e o padrão para lê-las
FORMATS = {
    'atual (2019+)': {'date': 'Data', 'time': 'Hora UTC', 'pattern': '%Y/%m/%d %H%M UTC'},
    'antigo (até 2018)': {'date': 'DATA (YYYY-MM-DD)', 'time': 'HORA (UTC)', 'pattern': '%Y-%m-%d %H:%M'},
}


def read_station_code(path):
    """Lê o código da estação (ex.: 'A612') nas linhas de cabeçalho do arquivo."""
    with open(path, encoding=ENCODING) as file:
        for _ in range(METADATA_LINES):
            key, value = file.readline().split(';')[:2]
            if key.startswith('CODIGO'):
                return value.strip()
    raise ValueError(f'Código da estação não encontrado no cabeçalho de {path}')


def detect_format(df, path):
    """Identifica o formato do arquivo pelas colunas de data e hora; devolve a chave de FORMATS."""
    for name, fmt in FORMATS.items():
        if fmt['date'] in df.columns and fmt['time'] in df.columns:
            return name
    raise ValueError(f'Formato de arquivo do INMET não reconhecido: {path}')


def read_inmet(path):
    """Lê os dados horários de um CSV do INMET, em qualquer um dos formatos de FORMATS.

    Acrescenta a coluna 'data_hora_utc' (timestamp com fuso UTC), juntando data e hora.
    O código de ausência (-9999) é lido como NaN, que será gravado como NULL no banco.
    """
    df = pd.read_csv(
        path, encoding=ENCODING, skiprows=METADATA_LINES, decimal=',', sep=';',
        na_values=[MISSING_VALUE],
    )
    fmt = FORMATS[detect_format(df, path)]
    df = df.drop(columns=[c for c in df.columns if c.startswith('Unnamed')])
    df['data_hora_utc'] = pd.to_datetime(
        df[fmt['date']] + ' ' + df[fmt['time']], format=fmt['pattern'], utc=True
    )
    return df


def to_long(df):
    """Converte do formato largo (uma coluna por variável) para o longo (uma linha por hora e variável).

    Mantém só as variáveis de VARIABLES, já com o código usado em dim_variavel.
    Horas sem dado ficam com valor NaN, que será gravado como NULL no banco.
    """
    missing = [column for column in VARIABLES if column not in df.columns]
    if missing:
        raise ValueError(f'Colunas esperadas não encontradas no arquivo: {missing}')
    long = df.melt(
        id_vars='data_hora_utc',
        value_vars=list(VARIABLES),
        var_name='variavel',
        value_name='valor',
    )
    long['variavel'] = long['variavel'].map(VARIABLES)
    return long