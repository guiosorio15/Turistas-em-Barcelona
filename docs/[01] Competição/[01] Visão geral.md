# More Than a Hack 2027 — visão geral

Equipa: **Turistas de la Nave**, cinco elementos. Organizadores: Metrica Sports, FC Barcelona e Mobile World Capital Barcelona, no contexto do Talent Arena.

## Resultado concreto
Gerar por algoritmo um CSV válido e reproduzível para todos os 199 319 frames do jogo Barcelona–Athletic, entregar código público e documento técnico até 2026-11-17.
Pretendemos superar a baseline oficial; ainda não há resultados de um modelo próprio.

**Referência real (2026-10-24):** a baseline oficial está em `spellF1` 0,2433 no jogo completo, mas uma equipa concorrente publicou **0,610** em 7 jogos DFL held-out com o mesmo tipo de dados. É esse o nível a bater, não a baseline. Ver `../[03] Investigação/[03] Concorrência pública.md`.

## Problema
`H` e `A` representam posse com bola em jogo; `D` representa interrupção. `X` é abstenção.
Uma bola dividida não cria um estado novo: mantém-se a última equipa até haver controlo adversário.
Um toque ou desvio não implica mudança de posse. Separar interrupções de trocas de equipa é essencial.

## Recursos e dificuldades
Tracking automático, duas câmaras, Smart Tagging e homografias. A bola falta em 41% dos frames avaliados; há fragmentação e trocas de identidade.
A referência temporal da submissão é o vídeo tático a 25 fps. Broadcast não está alinhado diretamente.
O dataset local inicial está incompleto; consultar `../ambiente/dataset.md`.

## Calendário oficial publicado
- Inscrições: 2026-10-01.
- Dados: 2026-10-20.
- Entrega: 2026-11-17.
- Resultados: antes de 2026-11-26.

Há uma fase inicial de posse e fases posteriores referidas na documentação oficial; não assumir que os critérios antigos de pitch se aplicam à fase 1. Aqui o ranking é quantitativo.

## Fontes
- [README oficial](https://github.com/metrica-sports/more-than-a-hack-2027)
- [Contexto da competição](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/OVERVIEW.md)
- [Desafio](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/CHALLENGE.md)
- [Regras](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md)
- [Entrega](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/SUBMISSION.md)
