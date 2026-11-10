# [00] Índice — Investigação

O que já se sabe antes de escrever uma linha de código. **Ler esta secção poupa semanas.**

| # | Documento | Para quê |
|---|---|---|
| [01] | [Estado da arte]([01]%20Estado%20da%20arte.md) | Papers, métodos e o que aproveitar de cada um |
| [02] | [Repositórios de referência]([02]%20Repositórios%20de%20referência.md) | Código existente, com estrelas e licença |
| [03] | [Concorrência pública]([03]%20Concorrência%20pública.md) | 20+ equipas já publicaram; números e abordagens |
| [04] | [Resultados negativos]([04]%20Resultados%20negativos.md) | O que já foi tentado e **não** funcionou |
| [05] | [Ideias]([05]%20Ideias.md) | Hipóteses ranqueadas, com teste e estado |
| [06] | [Métodos 2026-11-08]([06]%20Métodos%202026-11-08.md) | Varrimento de GitHub, papers, indústria e Reddit |

## As três conclusões que mudam a estratégia

1. **A referência externa é ~0,61, não 0,243.** Em 7 jogos DFL, uma equipa mediu ~**0,61**; não é o piso do jogo-alvo. O alvo verificado é 0,2433 (baseline full) e 0,3256 (público). Bater a baseline oficial é o primeiro marco; 0,61 é referência do protocolo DFL.
2. **A etiqueta é mecânica.** Vem do tracking *corrigido*, não de um analista: `D` onde a bola está morta, senão a equipa que o tracker nomeia. Estamos a imitar um tracker, não a decidir futebol.
3. **A métrica é segmentação.** `spellF1` conta posses inteiras; um frame a frame brilhante com flicker pontua zero. O descodificador vale tanto como as features.

## Ordem de leitura recomendada

[03] Concorrência → [04] Resultados negativos → [01] Estado da arte → [05] Ideias.
