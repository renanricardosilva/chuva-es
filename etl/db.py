"""Conexão com o banco de dados ambiental."""
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

load_dotenv()


def get_engine():
    """Cria a conexão (engine) com o banco, a partir das variáveis do arquivo .env."""
    url = URL.create(
        drivername='postgresql+psycopg',
        username=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        host=os.environ['PGHOST'],
        port=int(os.environ['PGPORT']),
        database=os.environ['PGDATABASE'],
    )
    return create_engine(url)