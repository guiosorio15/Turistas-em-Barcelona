# Avaliação e protocolo

**Estado:** vivo · **Este documento manda.** Se uma experiência não o respeita, o número não conta.

## O problema de fundo

Temos **17 posses** para verificar a pipeline e **nenhuma** para afinar. A tentação de olhar para os 5 minutos e escolher a variante que dá melhor número é exatamente o erro que a competição documenta (`smooth125` ganha nos 5 min, perde no jogo completo). É proibido pelas regras e é estatisticamente inútil.

## Protocolo oficial

### 1. Validação primária — **7 jogos DFL/Sportec** (`leave-one-match-out`)

- Cada jogo é pontuado por modelos treinados nos outros seis.
- ~3 000 posses no total → o sinal estatístico que os 5 minutos não dão.
- Métrica: `spellF1` (média dos IoU 0,3–0,7), com `macroF1` ao lado.
- **É o único número que usamos para decidir.**

### 2. Verificação de contrato — 5 minutos públicos

Serve **só** para:
- confirmar alinhamento de frames (`frame = round(segundos × 25)`);
- confirmar que o CSV valida (199 319 linhas, ordem, labels);
- confirmar a semântica (um toque não muda posse, `D` não tem dono).

**Não serve para:** escolher hiperparâmetros, janelas, pesos, custos de transição ou variantes.

**Regra prática:** se a decisão muda quando olhamos para os 5 minutos, a decisão está errada.

### 3. Sanidade no jogo completo (sem GT)

Sem olhar a etiqueta nenhuma:

| Verificação | Esperado | Porquê |
|---|---|---|
| Nº de posses previstas | 250–350 | baseline `smooth50` faz 669 (medido em 2026-10-25); o líder 293 |
| % de frames `D` | ~45–50 % | 106 min avaliados, ~55 de bola em jogo |
| Nº de paragens | ~108 (literatura) | Siegle & Lames 2012 |
| Concordância com `SET PIECES` | ≥90 % dos set pieces com recomeço a ±2 s | 58 set pieces |
| Concordância de fase com Smart Tagging | ≥0,75 nos frames vivos | o líder reporta 0,795 |
| Duração média de posse | ~10–15 s | GT público: 14,2 s |

Estas seis linhas detetam a maior parte dos erros graves **sem tocar no GT**.

## Métricas: o que cada uma paga

| | `spellF1` (ranking) | `macroF1` (desempate) |
|---|---|---|
| Unidade | posse inteira | frame |
| `X` numa frame avaliada | preenchido com a última label da parte → custa pouco no meio, muito na transição | conta como erro |
| Erro típico que pune | **sobre-segmentação** (posses a mais) | classes raras (`D` curto) |
| Sensibilidade a atraso | alta a 1 s | quase nula |

## Incerteza

- `spellF1` tem ruído ~**0,04** (banda medida); `macroF1` ~0,01.
- **Nunca** reportar diferenças menores que isso como "melhoria".
- Para decidir entre duas variantes: `leave-one-match-out` + intervalo bootstrap sobre posses (não sobre frames — os frames não são independentes).
- GT público: ±0,06 por posse. Inútil para comparar.

## Regras de ouro do registo

1. Toda a experiência tem **ID** (E1, E2…), hipótese, comando e resultado em `docs/[04] Método/[05] Plano de experimentos.md`.
2. Resultado negativo **também** se regista (→ `docs/[03] Investigação/[04] Resultados negativos.md`).
3. Sem comando reproduzível, o número não existe.
4. Nunca comparar dois números obtidos com protocolos diferentes.

## O que nunca fazemos

- Afinar no jogo-alvo, de qualquer forma, incluindo "só uns pesos".
- Escolher a variante pelo resultado público.
- Correr o scorer modificado.
- Reportar o melhor de N tentativas sem dizer que foram N.
