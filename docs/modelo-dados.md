# Modelo de dados: banco ambiental do ES (MVP)

Modelo dimensional, com uma tabela de fato de medições em formato longo e dimensões compartilhadas. Decisão registrada na [ADR 0003](decisoes/0003-modelo-de-dados.md).

```mermaid
erDiagram
    dim_fonte ||--o{ dim_estacao : "opera"
    dim_macrorregiao ||--|{ dim_microrregiao : "agrupa"
    dim_microrregiao ||--|{ dim_municipio : "agrupa"
    dim_municipio ||--o{ dim_estacao : "contém"
    dim_estacao ||--o{ f_medicao : "registra"
    dim_variavel ||--o{ f_medicao : "define"

    dim_fonte {
        smallint id_fonte PK
        text sigla UK "ex.: INMET"
        text nome
        text url
    }
    dim_variavel {
        smallint id_variavel PK
        text codigo UK "ex.: precipitacao"
        text nome
        text unidade "ex.: mm, °C"
        text agregacao "soma ou media"
    }
    dim_macrorregiao {
        smallint id_macrorregiao PK
        text nome
    }
    dim_microrregiao {
        smallint id_microrregiao PK
        text nome
        smallint id_macrorregiao FK
    }
    dim_municipio {
        integer id_municipio PK "código IBGE"
        text nome
        smallint id_microrregiao FK
        geometry geom "MultiPolygon, SIRGAS 2000"
    }
    dim_estacao {
        integer id_estacao PK
        text codigo UK "ex.: A612"
        text nome
        smallint id_fonte FK
        integer id_municipio FK
        text situacao "Operante ou Pane"
        numeric altitude_m
        date data_inicio_operacao
        geometry geom "Point, SIRGAS 2000"
    }
    f_medicao {
        integer id_estacao PK, FK
        smallint id_variavel PK, FK
        timestamptz data_hora_utc PK
        numeric valor "nulo = sem registro"
    }
```