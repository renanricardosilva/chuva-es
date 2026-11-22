# Retrospectiva — Sprint 3: Banco de dados ambiental

- **Período:** 15/11/2026 a 21/11/2026
- **Objetivo:** construir o MVP de um banco de dados ambiental do ES (PostgreSQL/PostGIS), pensado para integrar no futuro outras fontes e variáveis
- **Resultado:** objetivo atingido, com todo o compromisso entregue

## Revisão: o que foi entregue

- **Ambiente** (#21): PostgreSQL 18 e PostGIS 3.6 instalados e documentados em `docs/ambiente.md`.
- **Modelo de dados** (#22): modelo dimensional (esquema estrela), registrado na ADR 0003 e no diagrama `docs/modelo-dados.md`.
- **Tabelas** (#23): script `sql/01_criar_tabelas.sql`, testado num banco vazio.
- **Estações** (#24): 11 estações automáticas do INMET no ES, a partir do catálogo oficial.
- **Municípios e regionalização** (#25): 78 municípios (malha do IBGE), 10 microrregiões e 4 macrorregiões (Lei 9.768/2011), e cada estação ligada ao seu município por consulta espacial.
- **Medições** (#26): 1.685.952 medições horárias de chuva e temperatura, carga idempotente e relatório por estação e ano.
- **Validação** (#27): o banco reproduz o notebook de exploração da A612 em todos os números comparados (`docs/validacao-a612.md`).
- **Documentação** (#28): seção do banco no README, com a receita para recriá-lo do zero testada num banco descartável.
- **Fora do planejado:** PR de documentação da fonte e da data de obtenção da malha do IBGE; inclusão das estações A615 e A623, ausentes do catálogo do INMET; carga de 2019 a out/2026, além do período 2021–2025 previsto na #26.

## As promessas da Sprint 2

1. **Rodar Restart + Run All antes de todo commit de notebook:** cumprida. Na #27, o notebook foi rodado do zero e as saídas conferidas antes do commit.
2. **Fechar o notebook antes de trocar de branch:** cumprida.
3. **Marcar *(testado)* ou *(segundo...)* em toda afirmação de documentação:** cumprida em parte. O princípio apareceu nos documentos (a receita "testada em 21/11/2026", as datas de obtenção das bases, a validação), mas não como marcação sistemática.
4. **Trabalhar uma tarefa por vez:** cumprida quase sempre. O ritmo passo a passo funcionou; em alguns momentos, as instruções ainda vieram em blocos grandes.

## Velocidade

- **Planejado:** 36 pontos de compromisso + 13 de desafio (#29 e #30).
- **Entregue:** 36 pontos, todo o compromisso. O desafio não foi iniciado e volta ao backlog.
- O escopo ampliado da #26 (13 estações e 2019 a out/2026) não foi reestimado.

## O que funcionou

- **A organização, como um todo:** issues com critérios de aceite, quadro, branches e PRs deram clareza sobre o que fazer e sobre quando algo estava pronto.
- **Planning poker:** estimar em pontos relativos ajudou muito a dimensionar a sprint, e a estimativa se confirmou (36 de 36).
- **Revisar e testar pelo menos uma vez:** quase sempre revela alguma falha. Exemplos: a conferência dos critérios da #25 mostrou um item incompleto; o relatório da carga mostrou datas deslocadas pelo fuso; o teste da receita do README encontrou um comando que falharia.
- **Ler os critérios de aceite antes de começar:** adotado na #27 e na #28, depois de quase deixar o relatório da #26 incompleto.
- **Deixar o trabalho extra como desafio, e não como promessa:** o compromisso foi cumprido inteiro, sem a pressão de entregar tudo.

## O que travou

- **Abas abertas sem uso no VS Code:** um arquivo aberto numa aba foi salvo por cima da versão nova gravada no disco (README de `data/reference`, em 18/11). Depois disso, passei a fechar as abas que não estou usando.

## O que aprendi

- **Gestão de projetos:** cada vez mais fundo em Scrum e Kanban, num misto (Scrumban) que se ajusta a um projeto de uma pessoa só.
- **SQL:** junções no esquema estrela, `GROUP BY`, CTEs (`WITH`), `CASE`, `FILTER`, `string_agg`, intervalos semiabertos e a ordem lógica de execução de uma consulta.
- **GitHub:** o fluxo de issue, branch, commits, PR e merge virou rotina; `--amend` para corrigir a mensagem antes do push.
- **Aprendizados técnicos:** idempotência (chave primária + `ON CONFLICT`); formato longo (`melt`); fuso horário (guardar em UTC e converter explicitamente); diferença entre dado corrompido e problema de exibição (`length()`); precisão da malha municipal (21 m da divisa contra ~125 m de erro admitido); reconciliação entre dois caminhos que partem dos mesmos dados.

## Impacto no plano

- **A #29** passa a cobrir só a série de 2006 a 2018 (formato antigo dos CSVs, com `-9999`), porque 2019 e 2020 já foram carregados na #26.
- **A #30** (*views* SQL) ganhou motivação concreta: o mesmo bloco de chuva mensal se repete três vezes em `sql/validacao.sql`.
- **Nova decisão a registrar em ADR:** calendário civil × "dia pluviométrico" (9h às 9h) nas agregações diárias. Inclinação atual: calendário civil no painel público.
- **A Etapa 4** (robô diário) continua dependendo do acesso à API do INMET, que exige um Acordo de Cooperação Técnica: revisão da ADR 0002 no backlog.

## O que vou mudar na próxima sprint

- **Deixar abertas só as abas que estou usando**, para evitar alterações indesejadas nos arquivos.
- **Aperfeiçoar o SQL na prática:** nas consultas da próxima sprint, escrever a minha versão primeiro e só depois compará-la com a sugerida.
