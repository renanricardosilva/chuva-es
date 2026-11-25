# Ambiente de desenvolvimento

Como recriar o ambiente do projeto do zero, no Windows.

## Banco de dados

- **PostgreSQL 18.1** (Windows x64), instalado pelo instalador oficial da EDB ([postgresql.org/download/windows](https://www.postgresql.org/download/windows/)). Roda como serviço do Windows (`postgresql-x64-18`), na porta 5432.
- **PostGIS 3.6.2**, instalado pelo Stack Builder (Spatial Extensions → *PostGIS 3.6 Bundle for PostgreSQL 18*). A versão 3.6.2 foi preferida à 3.7.0 por estabilidade: a 3.7 ainda estava na primeira publicação (.0).
- No instalador do PostGIS, a opção *Create spatial database* fica desmarcada: o banco é criado manualmente, com o nome do projeto.

### Criar o banco

```
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d postgres -c "CREATE DATABASE ambiental_es;"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d ambiental_es -c "CREATE EXTENSION postgis;"
```

Verificação: `SELECT postgis_full_version();` no banco `ambiental_es` deve retornar a versão do PostGIS. O banco usa a codificação UTF8.

**Atenção à codificação no Windows:** o `psql` usa, por padrão, a codificação do terminal (WIN1252), e não a dos arquivos do projeto (UTF-8). Por isso, os scripts SQL começam com `SET client_encoding = 'UTF8';`; sem essa linha, os acentos são gravados corrompidos. Os acentos podem continuar aparecendo errados na **tela** do terminal, mas o dado gravado está correto.

**Saídas longas no `psql`:** o `psql` pagina os resultados longos e espera uma tecla para continuar. Para receber a saída inteira de uma vez, use a opção `-P pager=off`.

## Python

1. Criar e ativar o ambiente virtual (`.venv`) e instalar as dependências: `pip install -r requirements.txt`.
2. Copiar `.env.example` para `.env` e preencher a senha do banco. O `.env` não é versionado.
3. Testar a conexão, a partir da raiz do projeto: `python -m etl.check_connection`.

## Power BI

- **Power BI Desktop 2.159.1231.0** (64 bits, outubro de 2026).
- O painel está salvo como **Power BI Project** (`powerbi/chuva-es.pbip`): o relatório e o modelo ficam em arquivos de texto, que o Git consegue comparar. O modelo usa o formato TMDL (`powerbi/chuva-es.SemanticModel/definition/`).
- A opção **Data/hora automática** está desligada (*Opções → Arquivo atual → Carregamento de dados*), para o modelo não criar tabelas de calendário ocultas.

### Abrir o projeto e atualizar os dados

1. Ter o banco `ambiental_es` criado e carregado, com as views de `sql/04_views.sql`.
2. Abrir `powerbi/chuva-es.pbip` no Power BI Desktop.
3. Na primeira vez, o Power BI pede as credenciais do PostgreSQL (servidor `localhost`, banco `ambiental_es`): tipo de autenticação **Básico**, usuário `postgres` e a senha do banco. Desmarcar **"Usar a conexão criptografada"**, porque o PostgreSQL local não tem SSL configurado. A senha fica guardada no perfil do Windows, e não nos arquivos do projeto.
4. **Página Inicial → Atualizar** carrega os dados atuais do banco.

### O que não é versionado

O `.gitignore` exclui `powerbi/**/.pbi/cache.abf` (cópia local dos dados importados) e `powerbi/**/.pbi/localSettings.json` (configurações da máquina). Os dados vêm sempre do banco, na atualização.

## Melhorias futuras

- Criar um usuário próprio do projeto, com permissões limitadas, em vez de usar o usuário administrador `postgres`.
