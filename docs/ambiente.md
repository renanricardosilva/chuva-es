# Ambiente de desenvolvimento

Como recriar o ambiente do projeto do zero, no Windows.

## Banco de dados

- **PostgreSQL 18.1** (Windows x64), instalado pelo instalador oficial da EDB ([postgresql.org/download/windows](https://www.postgresql.org/download/windows/)). Roda como serviço do Windows (`postgresql-x64-18`), na porta 5432.
- **PostGIS 3.6.2**, instalado pelo Stack Builder (Spatial Extensions → *PostGIS 3.6 Bundle for PostgreSQL 18*). A versão 3.6.2 foi preferida à 3.7.0 por estabilidade: a 3.7 ainda estava na primeira publicação (.0).
- No instalador do PostGIS, a opção *Create spatial database* fica desmarcada: o banco é criado manualmente, com o nome do projeto.

### Criar o banco

```
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE ambiental_es;"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d ambiental_es -c "CREATE EXTENSION postgis;"
```

Verificação: `SELECT postgis_full_version();` no banco `ambiental_es` deve retornar a versão do PostGIS. O banco usa a codificação UTF8.

## Python

1. Criar e ativar o ambiente virtual (`.venv`) e instalar as dependências: `pip install -r requirements.txt`.
2. Copiar `.env.example` para `.env` e preencher a senha do banco. O `.env` não é versionado.
3. Testar a conexão, a partir da raiz do projeto: `python -m etl.check_connection`.

## Melhorias futuras

- Criar um usuário próprio do projeto, com permissões limitadas, em vez de usar o usuário administrador `postgres`.