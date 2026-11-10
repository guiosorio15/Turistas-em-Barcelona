# Turistas de la Nave — relatório técnico

**Estado: rascunho avançado. LOMO de 7 jogos concluído: 0,525 ± 0,037. E5/E2b/E5b negativos; E2 congelado.**

## 1. Abordagem

```text
ATD tático → features coletivas → GBM de 3 classes → Viterbi de 3 estados → CSV
```

- **Sem identidades de jogador.** O ATD tem 46 slots para 22 pessoas; todas as features são coletivas ou relativas ao slot.
- **Treino só em dados externos:** 7 jogos DFL/Sportec (CC-BY 4.0), 1 002 644 frames.
- **Degradação do treino:** 41% da bola em lacunas de 3–30 s, 5% dos jogadores em falta por frame, ruído de 0,2 m nas coordenadas. O objetivo é aproximar o ruído do tracker do jogo.
- **Modelo:** `HistGradientBoostingClassifier` (300 iterações, 31 folhas, learning rate 0,08), três classes `H/A/D`.
- **Descodificação:** Viterbi de 3 estados. Custos de transição 9 (H↔A) e 12 (entrar/sair de `D`), vindos da literatura aplicada; não foram afinados no jogo.
- **Inferência no jogo:** ATD tático, orientação por parte inferida pelo slot do guarda-redes da casa, `X` fora das duas partes avaliadas.
- **Velocidades:** a coluna `S` do DFL está em km/h e a do ATD do jogo em m/s. Jogadores são convertidos (÷3,6); a velocidade da bola é derivada da posição, em m/s, com rejeição de saltos acima de 40 m/s e mediana de 5 frames. Sem esta correção, o modelo previa 57% de `D` no jogo.

## 2. Dados

| Fonte | Uso | Nota |
|---|---|---|
| ATD tático do jogo | input da inferência | 199 319 frames; 46 slots; bola em falta em 43,1% de todos os frames e 40,7% em cada parte |
| Smart Tagging, homografia, vídeos | não usados nesta versão | o modelo atual é só tracking |
| 7 jogos DFL/Sportec | treino e validação | CC-BY 4.0; labels `BallPossession`/`BallStatus`; 1 002 644 frames |
| GT público (5 min) | apenas contrato e sanidade | 17 posses; nunca treino, afinação ou seleção |
| GT privado / dados humanos do jogo | não usados | proibido pelas regras |

Não foram usadas etiquetas humanas, correções manuais, dados de eventos deste jogo nem o vídeo fornecido no treino.

## 3. Resultados

| Experiência | `spellF1` | `macroF1` | Posses | Nota |
|---|---|---|---|---|
| Baseline `smooth50` | 0,3256 público | 0,6207 | 26 público / 669 completo | fallback |
| DFL J03WMX, período 1→2, limpo | 0,576 | 0,907 | 255 / 261 | referência superior |
| DFL J03WMX, período 1→2, degradado | **0,443** | 0,835 | 244 / 261 | métrica de decisão |
| Jogo completo, modelo dos 7 jogos | `?` | `?` | 415 | 43,1% `D`; 8,7 s |
| Público isolado, modelo dos 7 jogos | 0,5455 | 0,7696 | 27 / 17 | ±0,25; **não é seleção** |
| LOMO 7 jogos | **0,525 ± 0,037** | 0,868 | 323–376 / 370–511 | 7 folds; decisão |

O público tem 17 posses e um intervalo bootstrap de ±0,25; não ordena variantes. A decisão usa o DFL degradado. O score privado do jogo completo é desconhecido.

### Negativos medidos (DFL, 2026-11-08)

| Experiência | `spellF1` | Decisão |
|---|---|---|
| Bola fora pela posição crua (conf. 3/25/50) | 0,403 / 0,421 / 0,420 | não usar (N13) |
| Três classificadores (morto/vivo + dono) | 0,411 | não usar (N14) |
| E5b: 4 estados / p90 feature / etapa física | 0,435 / 0,428 / 0,396 | não usar (N15–N17) |

O GBM único + Viterbi mantém-se. O E4/HSMM fica adiado: o prior de durações do DFL não corresponde à convenção mais longa do jogo e, sem dados externos adequados, seria afinação no alvo.

### Trabalho futuro (pesquisa 2026-11-08)

O varrimento de 50+ repositórios, papers e indústria (`[03] Investigação/[06] Métodos 2026-11-08.md`) mostra que a lacuna do E2 está nas bordas/recomeços e na TCN/mais dados. Os componentes simples do **E5b** foram testados e não transferiram para o DFL (0,435/0,428/0,396 vs 0,443; N15–N17). O caminho com maior potencial restante é **E6** (TCN + SkillCorner); o E2 atual continua a submissão válida.

## 4. Limitações

- **Lacuna de convenção:** o DFL muda de posse ~9×/min vivo; o jogo ~4×/min. O modelo dos 7 jogos ainda produz 415 posses (esperado ~293) e 43,1% `D` (esperado ~45–50%).
- **E5/E2b/E5b negativos:** a regra de bola fora pela posição crua, a separação em três classificadores e os componentes do E5b (4 estados, p90, etapa física) pioraram o DFL; o E2 (GBM único + Viterbi) está congelado. E4/HSMM adiado sem prior externo adequado.
- **Sem vídeo:** não há tactical/broadcast MP4 no conjunto local; o modelo não depende deles, mas não explora close-ups nem áudio.
- **Amostra pública pequena:** 5 min e 17 posses; qualquer diferença abaixo de ~0,25 é ruído.
- **Artefacto treinado:** o modelo é um ficheiro treinado em DFL público; a reprodução do treino exige descarregar esse dataset. A inferência só exige o artefacto e o ATD fornecido.

## 5. Reprodução

```bash
uv sync --locked

# baseline oficial (fallback)
uv run --locked turistas reproduce

# modelo próprio — requer o ATD tático em data/tactical/
uv run --locked python scripts/predict_target.py \
  --model models/e1_dfl_v3.joblib \
  --output outputs/submissions/Turistas_de_la_Nave.csv

# contrato oficial
uv run --locked turistas validate outputs/submissions/Turistas_de_la_Nave.csv
```

Treino (dados externos):

```bash
uv sync --locked --extra notebooks
uv run --locked python scripts/fetch_dfl.py
uv run --locked --extra notebooks python scripts/train_model.py \
  --output models/e1_dfl_v3.joblib
```

O `data/` e o `outputs/` são locais e estão no `.gitignore`. O CSV final tem de ser regenerado a partir dos dados fornecidos e do artefacto versionado.

## 6. Conformidade

- Sem etiquetas manuais, correções humanas ou GT deste jogo.
- Treino, features, hiperparâmetros e custos de transição só em DFL/outros jogos.
- O GT público foi usado apenas para validar contrato, alinhamento e semântica.
- O scorer oficial não foi alterado.
- Nenhum dado restrito, vídeo ou derivado que o reconstrua foi incluído no repositório.
