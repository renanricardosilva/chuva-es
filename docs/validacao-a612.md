# Validação do banco: A612 (Vitória), 2021–2025

Issue #27 · Consultas: [`sql/validacao.sql`](../sql/validacao.sql) · Referência: [`notebooks/01-exploracao-vitoria.ipynb`](../notebooks/01-exploracao-vitoria.ipynb)

## Objetivo

Verificar se os dados carregados no banco reproduzem os resultados do notebook de exploração da estação de Vitória (A612). Os dois caminhos partem dos mesmos arquivos do INMET:

```
CSVs do INMET ──► pandas (notebook) ──────────────► resultados A
              └─► ETL (etl/) ──► PostgreSQL ──► SQL ──► resultados B
```

Se A = B, o ETL não perdeu, duplicou nem distorceu dados, e as análises podem passar a sair do banco.

## Convenção de tempo

O notebook agrupa anos e meses pela coluna `Data` do CSV, que está em **UTC**. Para a comparação, as consultas 1 a 4 também agrupam em UTC (`AT TIME ZONE 'UTC'`) e filtram o período com horários explícitos em UTC (`'2021-01-01 00:00+00'`). A consulta 5 mede o efeito de agrupar no horário de Vitória.

## Resultados

| # | Verificação | Notebook | Banco (SQL) | Resultado |
|---|---|---|---|---|
| 1 | Horas e horas sem registro de chuva, por ano | 43.824 h; sem registro: 1.082 / 431 / 18 / 3.486 / 204 | idem | ✅ idêntico |
| 2 | Completude mensal: válidos / baixa confiança / excluídos | 47 / 4 / 9 (60 meses) | 47 / 4 / 9, **com os mesmos meses** | ✅ idêntico |
| 3 | Total anual de chuva (só meses válidos) | 2025: 1.455,4 · 2021: 1.226,4 · 2022: 1.130,6 · 2023: 1.117,2 · 2024: 1.024,6 | idem | ✅ idêntico |
| 4 | Média, mínimo e máximo mensais (12 meses × 4 colunas) | tabela `monthly_mean` | idem | ✅ idêntico |

Na verificação 2, o caso-limite de maio de 2021 (completude de 74,6%) foi classificado como excluído nos dois caminhos: o critério é aplicado aos valores exatos, sem arredondamento.

Os mínimos e máximos da verificação 4 vêm de meses específicos (ex.: o máximo de novembro, 343,6 mm, é novembro de 2022). Por isso eles conferem totais mensais individuais, e não apenas médias.

**Conclusão:** com a mesma convenção de tempo, o banco reproduz o notebook em todos os números comparados.

## Divergências encontradas e explicadas

### 1. Mês em UTC × mês local (consulta 5)

Agrupando pelo mês de Vitória (`America/Sao_Paulo`) em vez do mês UTC, **18 dos 60 meses** mudam de total. A chuva das 21h à meia-noite do último dia de cada mês (horário local) pertence ao dia seguinte em UTC, e muda de mês. As maiores diferenças:

| Mês | UTC (notebook) | Local | Diferença |
|---|---|---|---|
| 2021-09 | 105,6 | 93,8 | −11,8 |
| 2021-08 | 80,6 | 92,0 | +11,4 |
| 2022-11 | 343,6 | 352,8 | +9,2 |
| 2022-12 | 327,2 | 318,0 | −9,2 |

- Pouco tempo não significa pouca chuva: uma única chuva forte no começo da noite pode mudar um total mensal em mais de 10%.
- O **total do período** (6.217,2 mm) é o mesmo nos dois agrupamentos: a chuva só troca de mês.
- **Nenhum mês muda de classe** de completude.
- Mudam alguns resultados do notebook: o mínimo de junho (11,2 → 15,2 mm), o máximo de novembro (343,6 → 352,8 mm) e o total válido de 2021 (1.226,4 → 1.221,8 mm). As conclusões (pico em novembro e dezembro, inverno seco, verão como a estação mais chuvosa) não mudam.

**Decisão:** o notebook usou UTC por simplificação. Para o painel, os agrupamentos por dia, mês e ano devem usar o **horário de Vitória**, como prevê a ADR 0003. A escolha entre o calendário civil e o "dia pluviométrico" (9h às 9h) fica para uma ADR futura.

### 2. Arredondamento de valores terminados em 5

Cinco médias mensais terminam exatamente em 5 na segunda casa decimal: março (134,75), abril (116,95), junho (43,55), julho (46,95) e outubro (129,75). O PostgreSQL arredonda o 5 para cima; o pandas guarda os números como `float` binário e o numpy arredonda para o par mais próximo. Nesta validação, os dois concordaram nos cinco casos, mas em parte por coincidência. **Recomendação:** em reconciliações futuras, comparar valores com duas ou mais casas decimais e arredondar só na apresentação.

### 3. Reprodutibilidade do notebook

O notebook selecionava os arquivos por `glob('*A612*')`. Quando a pasta passou a ter todos os anos (2006–2026), a seleção deixaria de pegar só 2021–2025. **Correção:** o período passou a ser declarado no código (`YEARS = range(2021, 2026)`). Depois da correção, o notebook rodado do zero reproduziu todos os seus resultados anteriores.

## Como reproduzir

```
psql -U postgres -d ambiental_es -f sql/validacao.sql
```

No notebook, a seção 8 calcula a referência por ano (verificação 1). As referências das verificações 2 a 4 estão nas seções 4 e 6.
