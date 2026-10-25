# [00] Índice — Método

Como vamos resolver o problema e, sobretudo, **como sabemos se melhorámos**.

| # | Documento | Estado |
|---|---|---|
| [01] | [Arquitetura]([01]%20Arquitetura.md) — o que existe e o alvo | vivo |
| [02] | [Features]([02]%20Features.md) — catálogo sem identidades | rascunho |
| [03] | [Decodificação temporal]([03]%20Decodificação%20temporal.md) — de probabilidades a posses | rascunho |
| [04] | [Avaliação e protocolo]([04]%20Avaliação%20e%20protocolo.md) — o contrato de honestidade | vivo |
| [05] | [Plano de experimentos]([05]%20Plano%20de%20experimentos.md) — fila de trabalho | vivo |
| [06] | [Relatório técnico]([06]%20Relatório%20técnico.md) — o documento da entrega | rascunho |

## A pipeline em cinco blocos

```
ATD (tático) ──► features por frame ──► probabilidades ──► decodificação ──► CSV
   + Smart Tagging / homografia / broadcast ─┘                   │
                                            durações e custos ◄─┘
```

1. **Entrada:** tracking tático (posições, velocidades, bola), metadados de equipa; opcionalmente Smart Tagging, homografia e broadcast.
2. **Features:** descritores **sem identidade** de jogador (o ATD não as tem), com contexto temporal antes/depois.
3. **Modelos por frame:** probabilidade de `morto/vivo`, de `H/A` quando vivo, e de `quem recomeça` quando morto.
4. **Decodificação:** escolher a sequência de estados que maximiza evidência − custo de transição, com durações plausíveis.
5. **Saída:** `frame,label` para os 199 319 frames, validado pelo scorer oficial.

## Princípio de desenho

> **Simples que sobrevive a 30 frames de erro > complexo que acerta no frame.**

O sistema tem de ser robusto a: bola ausente (41 %), slots que aparecem e desaparecem, e posses de 0,8 s.
