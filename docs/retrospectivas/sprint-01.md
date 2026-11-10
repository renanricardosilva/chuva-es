# Retrospectiva — Sprint 1: Fundação

- **Período:** 08/11/2026 a 10/11/2026
- **Objetivo:** concluir a Etapa 0 (repositório, registro de decisão, sonda do INMET)
- **Resultado:** objetivo atingido

## O que funcionou

Os testes funcionaram, mostrando que o caminho seguido não funciona e rejeitando a hipótese inicial. Elaborar hipóteses também se mostrou essencial, pois a sua testagem permitiu entender o que não é possível, abrindo caminho para novos horizontes.

## O que travou

- O entendimento inicial dos possíveis bloqueios do site do INMET, com respostas via protocolo HTTP. Entretanto, o bloqueio veio antes mesmo de se chegar nesse ponto;
- Erros de digitação também se mostraram travas, como nomear o diretório como "decisioes" ao invés de "decisoes";
- Editar arquivo depois do `push`;
- Falta de clareza sobre onde realizar cada passo e qual sequência, devido a ainda falta de compreensão e experiência sobre a ferramenta e o processo como um todo.

## O que aprendi

- Aprendi a explorar mais as alternativas possíveis sobre como seguir com um projeto;
- A organização do projeto pelo GitHub tem sido a maior e melhor novidade até o momento, unificando ferramentas e desenvolvimento em um único lugar;
- O ciclo issue → ramo → commit → PR → squash merge;
- GitHub Actions: gatilhos, steps, continue-on-error;
- Ler uma conexão por camadas (DNS → TCP → TLS → HTTP);
- Controle positivo e o fato de que “verde ≠ sucesso”.

## O que vou mudar na próxima sprint

Estabelecer rotina obrigatória, como sempre rodar git status para entender se há commits, por exemplo. Também irei explorar melhor as possibilidades, antes de apenas levantar hipóteses, como o fato de se ter API do INMET.
O plano mudou
Não editar arquivos de um ramo depois de abrir o PR sem fazer commit.