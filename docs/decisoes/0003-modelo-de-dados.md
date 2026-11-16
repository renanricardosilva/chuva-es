# 0003 — Modelo de dados: dimensional, com fato de medições em formato longo

- **Data:** 2026-11-16
- **Status:** aceita
- **Relação:** detalhada em [modelo de dados](../modelo-dados.md); base para as cargas da Sprint 3

## Contexto

O banco `ambiental_es` é o MVP de um banco de dados ambiental do ES, que deve receber, no futuro, fontes e variáveis diversas (qualidade do ar, alertas florestais, entre outras). No MVP, guarda chuva e temperatura das estações automáticas do INMET, com municípios e regionalização do estado.

O banco é usado quase só para leitura e análise, com consultas em SQL e um painel no Power BI. Ele precisa responder a perguntas como: qual foi a chuva total do mês passado numa região? Quais meses mais chovem? Qual foi o ano mais seco? Esta última exige saber quantas horas ficaram sem registro, porque a falta de dado não pode ser confundida com seca (como mostrou a análise da estação de Vitória em 2024).

## Decisão

1. **Modelo dimensional** (star schema): uma tabela de fato de medições e dimensões de contexto (estação, variável, fonte, município e regionalização).
2. **Fato de medições em formato longo:** uma linha por estação, variável e momento (`f_medicao`), e não uma coluna por variável. A unidade e a forma de agregação de cada variável (soma ou média) ficam na `dim_variavel`.
3. **Snowflake apenas na geografia:** estação → município → microrregião → macrorregião, cada nível em sua tabela, com as geometrias no PostGIS. Views achatam essa cadeia para o Power BI.
4. **Tempo em UTC:** o momento é guardado como `timestamptz`, em UTC, como vem do INMET. A conversão para a hora local é feita na leitura, com o fuso `America/Sao_Paulo`, que considera o horário de verão vigente até 2019.
5. **Ausência como nulo:** horas sem registro são gravadas com `valor` nulo, e não omitidas, para permitir calcular a completude diretamente em SQL.
6. **Geometrias em SIRGAS 2000** (EPSG:4674), o referencial geodésico oficial do Brasil, o mesmo da malha municipal do IBGE.
7. **Chave da medição:** estação + variável + momento, o que impede registros duplicados e torna as cargas idempotentes.

## Alternativas consideradas

- **Uma tabela de fato por variável** (`f_chuva`, `f_temperatura`, `f_pm10`): foi a primeira proposta. Descartada porque as tabelas teriam a mesma estrutura e o mesmo processo de origem (uma estação mede algo a cada hora); pela regra de uma tabela de fato por processo e granularidade, cabem num único fato com a dimensão de variável.
- **Formato largo** (uma coluna por variável): mais simples de consultar, mas cada variável nova exigiria alterar a estrutura da tabela, o que contraria o objetivo de um banco ambiental geral.
- **Modelo normalizado (3FN) como estrutura principal:** adequado a sistemas transacionais, com muitas alterações; o uso aqui é analítico.
- **Guardar a hora local:** descartado, porque a hora local muda com o horário de verão, o que gera horas repetidas ou inexistentes; o UTC é contínuo.
- **Omitir as horas sem registro:** economizaria espaço, mas esconderia a ausência e dificultaria o cálculo da completude.
- **Dimensão de tempo (calendário) e geometria das regiões:** adiadas (YAGNI); os agrupamentos temporais são feitos nas consultas, e a geometria das regiões pode ser calculada pela união dos municípios.

## Consequências

- O ETL precisa converter os CSVs do INMET (uma coluna por variável) para o formato longo.
- Consultas que comparam variáveis lado a lado exigem views; elas serão a interface com o Power BI.
- Novas variáveis da mesma natureza (medições em pontos de monitoramento) entram como novas linhas na `dim_variavel`, sem mudar a estrutura.
- Processos diferentes, como os alertas florestais, terão tabelas de fato próprias, compartilhando as dimensões geográficas e de fonte (dimensões conformadas), o que permite cruzar temas pelo lugar e pelo tempo.
- O volume previsto para o MVP (cerca de 4 milhões de linhas para 11 estações, 20 anos e 2 variáveis) é baixo para o PostgreSQL.