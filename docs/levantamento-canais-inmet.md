# Levantamento dos canais de dados do INMET

**Data do levantamento:** 13/11/2026
**Objetivo:** comparar as formas de obter dados do INMET, para embasar a ADR 0002 (acesso aos dados).

## Resumo comparativo

| Canal | Cobertura | Resolução | Atualização | Permite automação? | Acesso |
|---|---|---|---|---|---|
| Portal de dados históricos | Estações automáticas do Brasil, desde 2000 (A612: desde 2006) | Horária | Até 31/10/2026 (ano corrente parcial) *(testado)* | Não: o servidor recusa acesso por script *(testado)* | Download manual de ZIP anual, sem cadastro |
| BDMEP | Estações automáticas e convencionais do Brasil (data mais antiga: não verificada) | Horária, diária ou mensal | Quase em tempo real: dados de cerca de 1 h antes do processamento *(testado)* | Não: formulário, confirmação por e-mail, fila, um pedido por vez, link de 48 h *(testado)* | Formulário com e-mail; ZIP com o período pedido, enviado por link temporário |
| Tabela de dados das estações | | | | | |
| API | | | | | |

## Detalhes por canal

### Portal de dados históricos
- O [portal](https://portal.inmet.gov.br/dadoshistoricos) lista um arquivo ZIP por ano; cada ZIP traz um CSV por estação automática do Brasil.
- Cada CSV tem 8 linhas de metadados (região, código, coordenadas, data de fundação da estação) antes do cabeçalho das colunas; os registros são horários, em UTC. O formato está detalhado no [notebook de exploração](../notebooks/01-exploracao-vitoria.ipynb).
- Atraso de publicação: em 13/11/2026, o dado mais recente era de 31/10/2026, cerca de duas semanas antes *(testado)*.
- Acesso automatizado: a [sonda da Sprint 1](../.github/workflows/sonda-inmet.yml) mostrou que o servidor recusa requisições feitas por script (a partir do GitHub Actions e do próprio computador), enquanto o navegador funciona normalmente. O bloqueio depende do tipo de cliente, não da origem *(testado; ver [retrospectiva da Sprint 1](retrospectivas/sprint-01.md))*.
- Conclusão: canal adequado para a **carga histórica**, feita manualmente uma vez; inadequado para a **atualização diária**, por exigir download manual e ter atraso de semanas.

### BDMEP

- **Fluxo de acesso:** e-mail → formulário (separador decimal, resolução, tipo de estação, abrangência, período, variáveis e estações) → tela de confirmação → link de confirmação por e-mail → fila de processamento → e-mail de início → e-mail de conclusão com o link do arquivo. O link expira em 48 h, e só é permitido um pedido por vez.
- **Teste (13/11/2026):** estação A612, dados horários de 01 a 13/11/2026, três variáveis. Pedido às 20:44; e-mails de início e de conclusão às 21:22, ou seja, cerca de 40 minutos, quase todos de espera na fila *(testado)*. É provável que pedidos maiores demorem mais *(não testado)*.
- **Atualização:** o arquivo trouxe dados até 13/11, 23:00, o fim do período pedido.
- **Fuso horário:** o arquivo não indica o fuso. Como foi gerado às 21:22 (hora local) e contém dados das 23:00, as horas só podem estar em UTC (23:00 UTC = 20:00 local). Portanto, o BDMEP entregou dados de cerca de 1 h antes do processamento.
- **Formato diferente do portal:**

| | Portal | BDMEP |
|---|---|---|
| Metadados | 8 linhas | 9 linhas + 1 em branco |
| Codificação | latin-1 | UTF-8 |
| Data | `2021/01/01` | `2026-11-01` |
| Hora | `0000 UTC` | `0000` (sem indicar o fuso) |
| Nome das colunas | com acentos, espaço antes da unidade | sem acentos, sem espaço |
| Situação da estação | – | `Situacao: Operante` |

  Consequência: a função `read_inmet` do notebook não lê este arquivo; usar os dois canais exige duas leituras que produzam o mesmo formato.
- **Recomendação do próprio INMET:** a página inicial do BDMEP indica o portal para os pacotes anuais de todas as estações e a Tabela de Dados de Estação (sistema TEMPO) para dados horários de curta duração (até 6 meses) de uma estação.
- **Conclusão:** é o canal mais atualizado entre os testados até aqui e oferece resoluções horária, diária e mensal, mas o fluxo por e-mail e fila impede a automação. Serve para pedidos pontuais e para conferir dados recentes.

### Tabela de dados das estações

### API

## A API entrega dados horários das últimas 24 h das estações do ES?

## Conclusão para a ADR 0002