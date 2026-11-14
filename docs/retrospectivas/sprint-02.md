# Retrospectiva — Sprint 2: Acesso e primeiros dados

- **Período:** 11/11/2026 a 14/11/2026
- **Objetivo:** entender os dados do INMET e definir como obtê-los
- **Resultado:** objetivo atingido

## Revisão: o que foi entregue

- **Visão do produto e histórias de usuário** (#15): públicos, histórias 1 a 4 e limites declarados no README.
- **Exploração dos dados de Vitória** (#14): notebook com leitura dos arquivos, completude, investigação das falhas da estação e análises da chuva (2021–2025).
- **Levantamento dos canais do INMET** (#10): portal, BDMEP, Tabela e API testados, com evidências.
- **Pedido do token da API** (#12): enviado em 14/11/2026, em nome da SEAMA.
- **ADR 0002** (#13): portal para o histórico, API para os dados recentes, plano provisório.
- **Fora do planejado:** atualização do README (status e roteiro, #17) e ampliação do escopo da #14 com as análises da chuva.

## As promessas da Sprint 1

1. **Rodar `git status` antes de todo commit e de toda troca de branch:** cumprida em parte. Virou hábito antes dos commits (por exemplo, ao retomar o trabalho em 14/11, conferindo branch e push antes de seguir). Faltou antes do `git switch main` de 13/11, que travou na pasta `notebooks` por estar com o notebook aberto.
2. **Pesquisar a documentação antes de levantar hipóteses:** cumprida. Antes de testar a API, procurei o manual oficial (fora do ar) e fontes de terceiros, e o levantamento separou o que foi testado do que foi lido.
3. **Não editar arquivos de uma branch depois de abrir o PR sem fazer commit:** cumprida. Quando o escopo da #14 cresceu (análises de chuva, teste do -9999), as mudanças entraram como novos commits na mesma branch, atualizando o PR aberto, em vez de edições soltas.

## O que funcionou

- A organização em seguindo os princípios Scrum tem facilitado muito a evolução e compreensão do caminho a ser seguido
- Levantamento de hipóteses e sua testagem dá margem para explorar alternativas e poder compará-la, sem escolher uma aleatoriamente, mas pautado na experimentação
- Obtenção manual, por hora, tem funcionado, pois os dados foram adquiridos

## O que travou

- A falta de informação oficial sobre chave API do sistema
- Os NameError do notebook, por estado oculto e células fora de ordem
- Link sem retorno, necessitando investigação mais aprofundada

## O que aprendi

- API's e links oficiais de documentação podem quebrar 
- Documentar o código dá trabalho, mas é muito valioso
- O caminho se faz caminhando. Às vezes, vamos adaptando a rota de acordo com as necessidades vão surgindo

## Impacto no plano

- Modelagem do banco de dados subiu de prioridade
- Automatização bloqueada por falta de token

## O que vou mudar na próxima sprint

- Rodar Restart + Run All antes de todo commit de notebook;
- Fechar o notebook antes de trocar de branch;
- Marcar (testado) ou (segundo...) em toda afirmação de documentação;
- Trabalhar uma tarefa por vez, pedindo o próximo passo só depois de concluir o anterior.