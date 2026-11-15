"""Teste rápido da conexão com o banco ambiental_es."""
from sqlalchemy import text

from etl.db import get_engine

engine = get_engine()
with engine.connect() as conn:
    database = conn.execute(text('SELECT current_database();')).scalar()
    postgis = conn.execute(text('SELECT postgis_version();')).scalar()

print(f'Conectado ao banco: {database}')
print(f'PostGIS: {postgis}')