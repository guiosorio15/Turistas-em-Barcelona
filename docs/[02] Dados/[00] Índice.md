# [00] Índice — Dados

Tudo o que entra no sistema, o que promete e o que falha.

| # | Documento | Estado |
|---|---|---|
| [01] | [Pacote local]([01]%20Pacote%20local.md) — inventário, onde pôr, o que falta | vivo |
| [02] | [ATD e alinhamento]([02]%20ATD%20e%20alinhamento.md) — tracking automático, coordenadas, offsets | vivo |
| [03] | [Smart Tagging]([03]%20Smart%20Tagging.md) — 638 fases, 13 códigos, armadilhas | vivo |
| [04] | [Homografia e broadcast]([04]%20Homografia%20e%20broadcast.md) — a ponte para os pixels | vivo |

## O jogo em números

| | |
|---|---|
| Jogo | FC Barcelona (H) vs Athletic Club (A), LaLiga 2024-25, jornada 2 |
| Frames | 199 319 a 25 fps (~2 h 13 min) |
| Frames avaliados | **158 857** (1.ª parte 11 185–90 651; 2.ª 110 808–190 197) |
| Bola visível | 56,9 % de todos os frames · **59,3 % dos avaliados** |
| Slots de tracking | 46 para 22 jogadores, **sem identidade** |
| Smart Tagging | 638 instâncias automáticas |
| GT público | 5 min = frames 11 185–18 684, **17 posses** |

## As três frases que definem a dificuldade

1. **A bola falta em 41 % dos frames avaliados**, em blocos longos — não em frames soltos.
2. **A maior parte dos frames sem bola é bola morta**; o resto é multidão e bola no ar.
3. **As lacunas curtas já foram colmatadas pelo fornecedor**: quase não há lacunas entre 1 e 3 s, e sobram ~133 com 3 s ou mais.

Fonte: `vendor/mtah/DATA.md`; medições de lacunas confirmadas por duas equipas concorrentes (ver `docs/[03] Investigação/[03] Concorrência pública.md`).
