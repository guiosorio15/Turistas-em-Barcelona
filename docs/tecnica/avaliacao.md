# Avaliação

Ranking por `spellF1`: correspondência individual entre posses previstas e reais pela sobreposição temporal, média dos limiares IoU 0,3–0,7.
Uma posse é uma sequência máxima de `H` ou `A`; `D` interrompe a sequência.
`macroF1` mede frames nas classes `H/A/D` e é o primeiro desempate.
`X` penaliza macroF1; para spellF1 é preenchido com o último estado da mesma parte, com preenchimento inicial específico do scorer.

## Baselines publicadas
| Variante | spellF1 público | spellF1 jogo completo publicado |
| --- | --- | --- |
| smooth50 | 0,3256 | 0,2433 |
| smooth125 | 0,4242 | 0,2242 |

O facto de a ordem inverter mostra a fragilidade da amostra pública: cinco minutos e 17 posses.
Usar a janela pública apenas para verificar contrato, alinhamento e semântica. Não treinar, afinar nem selecionar variantes com ela.
A avaliação local não mede o resultado privado do jogo completo.

Executar `uv run --locked turistas evaluate`; resultados locais em `outputs/evaluation/`.
A definição exata está em `vendor/mtah/evaluation/possession_metrics.py`. Não modificar esse scorer.

Fontes: [EVALUATION.md](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md) e [RULES.md](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md).
