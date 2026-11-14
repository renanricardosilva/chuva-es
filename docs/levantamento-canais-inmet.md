# Levantamento dos canais de dados do INMET

**Data do levantamento:** 13 e 14/11/2026
**Objetivo:** comparar as formas de obter dados do INMET, para embasar a ADR 0002 (acesso aos dados).

## Resumo comparativo

| Canal | Cobertura | Resolução | Atualização | Permite automação? | Acesso |
|---|---|---|---|---|---|
| Portal de dados históricos | Estações automáticas do Brasil, desde 2000 (A612: desde 2006) | Horária | Até 31/10/2026 (ano corrente parcial) *(testado)* | Não: o servidor recusa acesso por script *(testado)* | Download manual de ZIP anual, sem cadastro |
| BDMEP | Estações automáticas e convencionais do Brasil (data mais antiga: não verificada) | Horária, diária ou mensal | Quase em tempo real: dados de cerca de 1 h antes do processamento *(testado)* | Não: formulário, confirmação por e-mail, fila, um pedido por vez, link de 48 h *(testado)* | Formulário com e-mail; ZIP com o período pedido, enviado por link temporário |
| Tabela de dados das estações (TEMPO) | Estações automáticas e convencionais, por estado | Horária, todas as variáveis | Tempo quase real: em 14/11 às ~11:48 (local), último registro às 11:00 local (14:00 UTC) *(testado)* | Não: página protegida por reCAPTCHA *(testado)* | Na tela, sem cadastro; CSV gerado no navegador; até 6 meses por consulta |
| API (apitempo) | Lista de estações automáticas sem token; dados horários por estação apenas com token *(segundo fontes de terceiros)* | Horária e diária *(segundo fontes de terceiros)* | Não verificada (requer token) | Sim, é o canal previsto para acesso programático, mas exige token | Token solicitado ao INMET; canal de solicitação não confirmado em fonte oficial |

## Detalhes por canal

### Portal de dados históricos
- O [portal](https://portal.inmet.gov.br/dadoshistoricos) lista um arquivo ZIP por ano; cada ZIP traz um CSV por estação automática do Brasil.
- Cada CSV tem 8 linhas de metadados (região, código, coordenadas, data de fundação da estação) antes do cabeçalho das colunas; os registros são horários, em UTC. O formato está detalhado no [notebook de exploração](../notebooks/01-exploracao-vitoria.ipynb).
- Atraso de publicação: em 13/11/2026, o dado mais recente era de 31/10/2026, cerca de duas semanas antes *(testado)*.
- Acesso automatizado: a [sonda da Sprint 1](../.github/workflows/sonda-inmet.yml) mostrou que o servidor recusa requisições feitas por script (a partir do GitHub Actions e do próprio computador), enquanto o navegador funciona normalmente. O bloqueio depende do tipo de cliente, não da origem *(testado; ver [retrospectiva da Sprint 1](retrospectivas/sprint-01.md))*.
- Conclusão: canal adequado para a **carga histórica**, feita manualmente uma vez; inadequado para a **atualização diária**, por exigir download manual e ter atraso de semanas.

### BDMEP

- **Fluxo de acesso:** e-mail → formulário (separador decimal, resolução, tipo de estação, abrangência, período, variáveis e estações) → tela de confirmação → link de confirmação por e-mail → fila de processamento → e-mail de início → e-mail de conclusão com o link do arquivo. O link expira em 48 h, e só é permitido um pedido por vez.
- **Teste (13/11/2026):** estação A612, dados horários de 01 a 13/11/2026, três variáveis. Pedido às 20:44; e-mails de início e de conclusão às 21:22, ou seja, cerca de 40 minutos, quase em todos de espera na fila *(testado)*. É provável que pedidos maiores demorem mais *(não testado)*.
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

### Tabela de dados das estações (sistema TEMPO)

- **Acesso:** na [Tabela de Dados das Estações](https://tempo.inmet.gov.br/TabelaEstacoes), escolhe-se o tipo de estação, o estado, a estação e o período (máximo de 6 meses). A tabela aparece na hora, sem cadastro nem e-mail, e o botão "Baixar CSV" gera o arquivo no próprio navegador.
- **Atualização:** em 14/11/2026, consultada por volta das 11:48 (hora local), a tabela trazia dados até as 11:00 local (14:00 UTC), um atraso inferior a 1 hora *(testado)*.
- **Armadilha das horas futuras:** quando o período inclui o dia corrente, as horas que ainda não ocorreram aparecem como linhas vazias. Linha vazia, aqui, não significa necessariamente falha da estação.
- **Mesma base do BDMEP:** comparando os arquivos dos dois canais para a A612 (01 a 13/11/2026), chuva e temperatura são idênticas nas 312 horas *(testado)*.
- **Formato:** um terceiro formato, diferente do portal e do BDMEP: sem metadados, UTF-8 com BOM, valores entre aspas, data `01/11/2026`, hora na coluna "Hora (UTC)" e nomes de coluna abreviados (ex.: `Chuva (mm)`).
- **Automação:** a página usa reCAPTCHA invisível, que não interrompe o uso humano, mas indica que o acesso automatizado não é previsto.
- **Conclusão:** é o canal mais prático para consultas humanas de dados recentes (inclusive das últimas horas), e o próprio INMET o recomenda para dados horários de até 6 meses. Não é adequado para automação.

### API (apitempo.inmet.gov.br)

- **Documentação oficial indisponível:** em 14/11/2026, o endereço do manual da API no portal retornava erro 404, e a seção "Manuais" do portal retornava erro interno do servidor *(testado)*. As informações sobre rotas e token vêm de projetos de terceiros e precisam ser confirmadas.
- **Lista de estações, sem token:** `https://apitempo.inmet.gov.br/estacoes/T` retorna um JSON com as estações automáticas e seus metadados, incluindo a situação (`CD_SITUACAO`: Operante ou Pane), o estado, o código e a data de início de operação *(testado)*.
- **Dados horários, sem token:** `https://apitempo.inmet.gov.br/estacao/2026-11-13/2026-11-14/A612` retorna **HTTP 204 (sem conteúdo)** *(testado, pelas Ferramentas do Desenvolvedor)*. Como a Tabela de Dados das Estações mostra dados da A612 nesse mesmo período, a ausência não é de dados, e sim de acesso: sem token, a rota não os entrega.
- **Token:** segundo projetos de terceiros, as rotas de dados exigem um token, solicitado ao INMET por e-mail. As fontes divergem quanto ao canal de solicitação, o que deve ser confirmado junto ao INMET (issue #12).
- **Ressalva do INMET, válida para todos os canais:** os dados das estações automáticas são brutos e não passam por processo de consistência, segundo [nota oficial do INMET](https://portal.inmet.gov.br/noticias/saiba-como-acessar-os-dados-meteorol%C3%B3gicos-dispon%C3%ADveis-no-site-do-inmet).
- **Conclusão:** é o único canal previsto para acesso automatizado, e por isso o candidato natural para o robô diário. Mas depende de um token ainda não obtido e de uma documentação hoje indisponível, o que é um risco para o projeto.

## A API entrega dados horários das últimas 24 h das estações do ES?

**Sem token, não:** a rota de dados horários retorna HTTP 204 (sem conteúdo), embora os dados existam (verificado na Tabela de Dados das Estações). **Com token, provavelmente sim**, segundo projetos de terceiros, mas isso só poderá ser verificado após a obtenção do token (issue #12).

Enquanto isso, a Tabela de Dados das Estações e o BDMEP já entregam dados com menos de 1 hora de atraso, mas apenas para consulta humana.

## Estações automáticas do ES

Segundo a lista de estações da API (`/estacoes/T`, consultada em 14/11/2026), o ES tem **11 estações automáticas**: 9 operantes (Afonso Cláudio, Alegre, Linhares, Marilândia, Presidente Kennedy, Santa Teresa, São Mateus, Venda Nova do Imigrante e Vitória) e 2 em pane (Ecoporanga e Vila Velha). O formulário do BDMEP lista 14 estações do ES; as 3 a mais (Alfredo Chaves, Ilha de Trindade e Nova Venécia) não constam da lista atual, provavelmente por estarem desativadas, com histórico mantido no BDMEP.

## Conclusão para a ADR 0002

- **Carga histórica:** pelo portal de dados históricos, com download manual dos ZIPs anuais (desde 2000). O servidor recusa acesso automatizado, mas a carga histórica é feita uma única vez.
- **Atualização diária:** o único canal previsto para automação é a API, que exige um token ainda não obtido (sem ele, a rota de dados retorna HTTP 204). A automação depende da issue #12.
- **Enquanto o token não chega:** o histórico vem do portal (na consulta de 13/11/2026, os dados iam até 31/10/2026), e os dados recentes podem ser obtidos manualmente na Tabela de Dados das Estações, que tem atraso inferior a 1 hora.
- **Riscos:**
  - documentação oficial da API indisponível (em 14/11/2026);
  - token sem prazo de obtenção e com canal de solicitação não confirmado;
  - formatos diferentes entre portal, BDMEP e Tabela, o que exige leituras distintas no ETL;
  - atualização manual diária, que depende de disciplina e pode ser interrompida;
  - dados brutos, sem validação pelo INMET.

  ## Fontes de terceiros consultadas

Informações não confirmadas em fonte oficial, usadas apenas como pistas:

- [ThiagoRBM/API_INMET](https://github.com/ThiagoRBM/API_INMET): relata o limite de 6 meses por consulta, desde cerca de maio de 2022.
- [monitorelnino, PR #386](https://github.com/monitorelnino/monitorelnino/pull/386): lista de estações (`/estacoes/T`) acessível sem token; token pedido à Central de Serviços do INMET.
- [monitorelnino, PR #401](https://github.com/monitorelnino/monitorelnino/pull/401): rotas com token e solicitação por e-mail a `cadastro.act@inmet.gov.br`.
- [alanmauro-oneagro/monitoresporos, PR #13](https://github.com/alanmauro-oneagro/monitoresporos/pull/13): relatos divergentes sobre a rota de dados horários sem token em 2026.