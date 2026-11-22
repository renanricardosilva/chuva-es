# Processo de trabalho

Como o projeto é conduzido: um Scrum adaptado para uma pessoa, com o GitHub como ferramenta central.

## Papéis

- **Product Owner e desenvolvedor:** Renan Ricardo Silva, que define as prioridades, toma as decisões de produto e executa o trabalho.
- **Scrum Master e revisão técnica:** apoio de um assistente de IA, que conduz os rituais, revisa código, textos e decisões, e propõe alternativas.

## Sprints

- **Duração:** uma semana.
- **Planejamento:** cada sprint tem um **objetivo** (o que estará pronto e demonstrável no fim) e um **backlog** de issues, registrados numa milestone do GitHub.
- **Compromisso e desafio:** o backlog separa o **compromisso** (o que define o sucesso da sprint) das metas de **desafio**, marcadas com a label `stretch`, feitas apenas se sobrar tempo.
- **Encerramento:** revisão (o que foi entregue, comparado ao objetivo) e retrospectiva (como foi o trabalho e o que muda), registrada em `docs/retrospectivas/`.

## Estimativa: planning poker

- Cada issue recebe **pontos** na sequência de Fibonacci (1, 2, 3, 5, 8, 13), registrados no campo **Points** do quadro.
- Os pontos são **relativos, não horas**: uma issue de 8 é cerca do dobro de uma de 3. A sequência cresce em saltos porque, quanto maior a tarefa, maior a incerteza.
- **Velocidade:** a soma dos pontos das issues entregues numa sprint. É conferida na retrospectiva e usada para calibrar o planejamento seguinte.

## Fluxo de uma issue

1. A issue nasce com **critérios de aceite verificáveis** e com as dependências registradas (*Blocked by*).
2. Ao começar, o cartão vai para **In Progress**, e o trabalho acontece numa branch própria.
3. Os commits seguem os [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`...).
4. O PR descreve o que entrega e fecha a issue com `Closes #N`.
5. Antes do merge: revisão do PR e conferência dos critérios de aceite.
6. **Squash and merge**, exclusão da branch e atualização da `main` local.

## Definição de pronto

Uma issue só está pronta quando:

- todos os critérios de aceite foram verificados e marcados;
- o trabalho está integrado à `main` por um PR revisado;
- a documentação afetada foi atualizada.

## Decisões

Decisões de arquitetura e de método são registradas como ADRs em `docs/decisoes/`, com contexto, decisão, alternativas e consequências.

## Histórico de velocidade

| Sprint | Período         | Planejado         | Entregue                                         |
|--------|-----------------|-------------------|--------------------------------------------------|
| 1      | 08 a 10/11/2026 | –                 | – (antes do planning poker)                      |
| 2      | 11 a 14/11/2026 | –                 | ≈ 26 (estimado depois)                           |
| 3      | 15 a 21/11/2026 | 36 + 13 (desafio) | 36 (todo o compromisso; desafio não iniciado)    |