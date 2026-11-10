# Plano de experimentos

**Estado:** vivo · fila de trabalho, por ordem de dependência

Cada linha é uma experiência com ID, hipótese e critério de decisão. Só se avança quando a anterior tem número.

| ID | Experiência | Depende de | Métrica de decisão | Estado |
|---|---|---|---|---|
| **E0** | Verificar o pacote de dados (9 assets) e correr a baseline real | download | `check-data` limpo | **concluído 2026-10-25** |
| **E1** | Loader DFL + degradação + `leave-one-match-out` | E0 | pipeline corre nos 7 jogos | **concluído 2026-11-07**; LOMO 0,525 ± 0,037 |
| **E2** | Baseline aprendida: GBM de 3 classes + Viterbi de custo fixo | E1 | `spellF1` DFL (esperado ~0,58–0,61) | **em curso** — 0,443 no split J03WMX; **LOMO 0,525 ± 0,037** |
| **E2b** | Três classificadores (morto/vivo, dono, recomeço) + Viterbi | E2 | `spellF1` DFL | **negativo 2026-11-08** — 0,411 vs 0,443; N14 |
| **E3** | Ablação de features (só bola / só forma / ambas / + contexto temporal) | E2 | `spellF1` DFL | a fazer |
| **E4** | Descodificador: custo fixo vs **HSMM com durações aprendidas** | E2 | `spellF1` DFL + nº de posses | adiado — sem prior externo adequado; N11 |
| **E5** | Deteção de **bola fora** e refinamento de bordas | E4 | erro de borda (frames) + `spellF1` DFL | **negativo 2026-11-08** — 0,403–0,421 vs 0,443; N13 (regra crua) |
| **E5b** | Borda/recomeço: p90 coletivo, strike do set piece, snap ao toque, Viterbi de 4 estados | E5, E2 | `spellF1` DFL + `D` F1 + nº posses | **negativo 2026-11-08** — 0,435/0,428/0,396 vs 0,443; N15–N17 |
| **E6** | **Modelo de sequência** (TCN/Transformer) sobre as mesmas features | E3 | `spellF1` DFL | a fazer — TCN é o melhor externo (Agamemnon); ver [06] |
| **E7** | **Ensemble** DFL + auto-supervisionado | E4, E6 | `spellF1` DFL | a fazer |
| **E8** | **Self-training** no jogo-alvo (1 ronda) | E7 | `spellF1` DFL + sanidade no jogo | a fazer |
| **E9** | Alinhamento automático do broadcast + sinal de close-up | E4 | `spellF1` DFL (pesos fora da janela pública) | a fazer |
| **E10** | Áudio/silvo, se existir faixa áudio | E0 | erro de borda | por verificar |
| **E11** | Detetor próprio de bola em oclusões | E5 | `spellF1` DFL | **baixa prioridade** |

## Critério de paragem (anti-perfeccionismo)

- Se E2 já estiver ≥0,60 em DFL, **congelar** a pipeline e dedicar o tempo a E4/E5 (bordas e durações), que é onde os outros não estão.
- Se E5 não der ganho em DFL, não insistir: registar como negativo.
- Nada de E11 antes de E4/E5/E6 estarem fechados.

## Calendário de trabalho (23 dias até à entrega, a partir de 2026-10-25)

| Semana | Foco |
|---|---|
| 25–27 out | E0 concluído; E1–E2: loader DFL e primeira baseline honesta |
| 28–31 out | E3–E4: ablações e descodificador com durações |
| 1–5 nov | E5: bordas e bola fora (maior oportunidade) |
| 6–10 nov | E6–E7: sequência e ensemble |
| 11–14 nov | E8–E9: adaptação e broadcast; congelar |
| 15–17 nov | Regenerar CSV, relatório, validação final, submeter |

## Revisão de 2026-11-08 (pesquisa)

O varrimento de 50+ repositórios, papers e indústria (`../[03] Investigação/[06] Métodos 2026-11-08.md`) mostra que os líderes combinam GBM/TCN + Viterbi + degradação + bordas/recomeços + mais dados externos (SkillCorner). O nosso E5 era a regra crua; os líderes usam p90 coletivo, strike do set piece, last-touch (SALT 2025), snap ao contacto e Viterbi de 4 estados (Suleyman, Agamemnon, Frame Control). E5b foi testado e é negativo (N15–N17); resta o E6 (TCN + SkillCorner). O E2 continua fallback e a submissão atual é válida.

## Registo de execuções

| Data | ID | Comando | Resultado | Nota |
|---|---|---|---|---|
| 2026-10-24 | — | `uv run --locked turistas evaluate` | baseline pública reproduzida | ver `outputs/evaluation/` |
| 2026-10-24 | E0 | download do pacote | concluído depois | ZIPs + MP4 em `~/Downloads` |
| 2026-10-25 | E0 | `turistas check-data` + `turistas reproduce` | 9/9 assets; 199 319 linhas; 669 posses; 35,9% `D` | CSV byte-a-byte igual ao oficial (`sha256 6d4e04b8...`) |
| 2026-10-25 | E0 | `turistas evaluate --results outputs/submissions --bootstrap 1000` | `spellF1` 0,3256; `macroF1` 0,6207; IC 0,214–0,447 | 17 posses; não usar para escolher variantes |
| 2026-11-07 | E1 | `uv run --locked python scripts/fetch_dfl.py` | 7 jogos DFL; assets do jogo 7/9 | DFL CC-BY; caches locais |
| 2026-11-07 | E2 | `uv run --locked --extra notebooks python scripts/run_e1.py --match J03WMX --degrade` | `spellF1` 0,443; 244 posses previstas vs 261 | split período 1→2 |
| 2026-11-07 | E2 | `uv run --locked --extra notebooks python scripts/train_model.py` | 1 002 644 frames; 123 features | 7 jogos; artefacto local |
| 2026-11-07 | E2 | `uv run --locked python scripts/predict_target.py --model outputs/models/e1_dfl_v3.joblib` | 43,1% `D`; 415 posses; 0,5455 público | full-match + sanidade; público não seleciona |
| 2026-11-07 | E1 | `uv run --locked --extra notebooks python scripts/run_lomo.py --degrade` | 0,525 ± 0,037; macro 0,868 | 7 folds; concluído |
| 2026-11-08 | E5 | `run_e1.py --ball-out --ball-out-confirmation 3/25/50` | 0,403 / 0,421 / 0,420 | negativo; N13 |
| 2026-11-08 | E2b | `run_e1.py --three-classifiers` | 0,411; macro 0,827 | negativo; N14 |
| 2026-11-08 | — | `uv run --locked turistas evaluate` | 4 baselines; 9 testes | CLI robusto a `[01]` |
