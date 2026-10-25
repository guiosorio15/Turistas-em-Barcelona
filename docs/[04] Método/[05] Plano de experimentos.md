# Plano de experimentos

**Estado:** vivo · fila de trabalho, por ordem de dependência

Cada linha é uma experiência com ID, hipótese e critério de decisão. Só se avança quando a anterior tem número.

| ID | Experiência | Depende de | Métrica de decisão | Estado |
|---|---|---|---|---|
| **E0** | Verificar o pacote de dados (9 assets) e correr a baseline real | download | `check-data` limpo | **concluído 2026-10-25** |
| **E1** | Loader DFL + degradação + `leave-one-match-out` | E0 | pipeline corre nos 7 jogos | a fazer — **timebox 2 dias** |
| **E2** | Baseline aprendida: 3 classificadores + Viterbi de custo fixo | E1 | `spellF1` DFL (esperado ~0,58–0,61) | a fazer |
| **E3** | Ablação de features (só bola / só forma / ambas / + contexto temporal) | E2 | `spellF1` DFL | a fazer |
| **E4** | Descodificador: custo fixo vs **HSMM com durações aprendidas** | E2 | `spellF1` DFL + nº de posses | a fazer |
| **E5** | Deteção de **bola fora** e refinamento de bordas | E4 | erro de borda (frames) + `spellF1` DFL | a fazer |
| **E6** | **Modelo de sequência** (TCN/Transformer) sobre as mesmas features | E3 | `spellF1` DFL | a fazer |
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

## Registo de execuções

| Data | ID | Comando | Resultado | Nota |
|---|---|---|---|---|
| 2026-10-24 | — | `uv run --locked turistas evaluate` | baseline pública reproduzida | ver `outputs/evaluation/` |
| 2026-10-24 | E0 | download do pacote | concluído depois | ZIPs + MP4 em `~/Downloads` |
| 2026-10-25 | E0 | `turistas check-data` + `turistas reproduce` | 9/9 assets; 199 319 linhas; 669 posses; 35,9% `D` | CSV byte-a-byte igual ao oficial (`sha256 6d4e04b8...`) |
| 2026-10-25 | E0 | `turistas evaluate --results outputs/submissions --bootstrap 1000` | `spellF1` 0,3256; `macroF1` 0,6207; IC 0,214–0,447 | 17 posses; não usar para escolher variantes |
