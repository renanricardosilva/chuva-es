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

1. **Rodar `git status` antes de todo commit e de toda troca de branch:** cumprida em parte. Virou hábito antes dos commits (por exemplo, ao retomar o trabalho em 14/11, conferindo a branch e o push antes de seguir). Faltou antes do `git switch main` de 13/11, que travou na pasta `notebooks` por estar com o notebook aberto.
2. **Pesquisar a documentação antes de levantar hipóteses:** cumprida. Antes de testar a API, procurei o manual oficial (fora do ar) e fontes de terceiros, e o levantamento separou o que foi testado do que foi lido.
3. **Não editar arquivos de uma branch depois de abrir o PR sem fazer commit:** cumprida. Quando o escopo da #14 cresceu (análises de chuva, teste do -9999), as mudanças entraram como novos commits na mesma branch, atualizando o PR aberto.

## O que funcionou

- **Organização no Scrum:** issues com critérios de aceite, quadro e PRs deram clareza sobre o que fazer a seguir e sobre quando algo estava realmente pronto.
- **Hipóteses testadas, não escolhidas:** levantar hipóteses e testá-las permitiu comparar alternativas com base em experimentos, não em palpites. Inclusive registrando as que caíram, como a da "retomada à tarde" do dia 17 de maio de 2022.
- **Obtenção manual, por enquanto:** os dados necessários foram obtidos (portal, BDMEP e Tabela), o que permitiu avançar sem esperar o token.

## O que travou

- **Falta de informação oficial sobre a API:** manual fora do ar e canal de pedido do token não confirmado.
- **`NameError` no notebook:** estado oculto e células fora de ordem, até a reorganização com Restart + Run All.
- **Rota da API sem retorno:** o navegador não mostrava nada; só com as Ferramentas do Desenvolvedor foi possível ver que a resposta era HTTP 204.
- **Muitos passos de uma vez:** em alguns momentos, o volume de instruções atrapalhou mais do que ajudou.

## O que aprendi

- **Links e APIs oficiais podem quebrar ou mudar:** por isso o levantamento registra a data e o que foi testado.
- **Documentar dá trabalho, mas vale:** o notebook virou um relatório que outra pessoa consegue ler e reproduzir.
- **O caminho se faz caminhando:** a rota se ajusta conforme as necessidades aparecem, desde que cada mudança fique registrada.
- **Aprendizados técnicos:** completude de dados e critério de exclusão; teste de hipóteses com previsão antes de rodar; refatoração, funções e a "regra de três"; horários em UTC; códigos HTTP e as Ferramentas do Desenvolvedor do navegador.

## Impacto no plano

- **A modelagem do banco de dados (Etapa 3) subiu de prioridade** e foi movida para antes do robô no roteiro.
- **A automação (Etapa 4) está bloqueada até a obtenção do token** da API, pedido em 14/11/2026.

## O que vou mudar na próxima sprint

- Rodar **Restart + Run All** antes de todo commit de notebook.
- **Fechar o notebook** antes de trocar de branch.
- Marcar *(testado)* ou *(segundo...)* em toda afirmação de documentação.
- Trabalhar **uma tarefa por vez**, pedindo o próximo passo só depois de concluir o anterior.