"""Leitura dos arquivos CSV de dados horários das estações automáticas do INMET."""
import pandas as pd

ENCODING = 'latin-1'
METADATA_LINES = 8  # linhas de cabeçalho antes da tabela (região, UF, estação, código...)

# Colunas do INMET carregadas no banco → código da variável em dim_variavel
VARIABLES = {
    'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'precipitacao',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'temperatura_ar',
}


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