# Estado da arte

**Estado:** vivo · último varrimento: 2026-10-24 (arXiv + GitHub + imprensa técnica)

Ler por esta ordem: primeiro o que **valida o desenho**, depois o que **inspira**, depois o que só **contextualiza**.

## Núcleo — o problema exato que temos

| Trabalho | Ano | O que faz | O que aproveitar |
|---|---|---|---|
| **Link & Hoernig, *Individual ball possession in soccer*** — PLOS ONE, doi:10.1371/journal.pone.0179953 | 2017 | Suavização RTS; *kick detection* por máximo local de aceleração da bola (≥4 m/s²); previsão da bola a 1 s; rede bayesiana para "controlo". 60 jogos da Bundesliga, 69 667 intervalos. **F=0,88** (ação) e **F=0,83** (posse) | O método clássico, validado, e o vocabulário correto (IBP/IBA/IBC/TBP). É a formalização das nossas notas "Modelo de Posse/Modelo de Passe" |
| **PathCRF: Ball-Free Soccer Event Detection via Possession Path Inference** — KDD 2026, arXiv:2602.12080 | 2026 | Modela 22 jogadores como **grafo dinâmico totalmente ligado**; a posse é escolher **uma aresta** por instante; CRF proíbe transições impossíveis; decodificação por **Viterbi**. **Não usa a bola** | A formalização mais limpa do problema — e a prova de que se pode inferir posse sem bola. Código: `hyunsungkim-ds/pathcrf` |
| **Vidal-Codina et al., *Automatic event detection in football using tracking data*** — Sports Engineering 25:18 | 2022 | Árvore de decisão determinística para extrair eventos de tracking | Estrutura para regras auditáveis (passes, recuperações) sem ML |
| **Bassek et al., *An integrated dataset of spatiotemporal and event data in elite soccer*** — Scientific Data 12:195, doi:10.1038/s41597-025-04505-y | 2025 | 7 jogos oficiais DFL/Sportec, 25 Hz, tracking + eventos, **CC-BY 4.0** | O nosso conjunto de **treino e validação** (dados de outros jogos = permitido) |
| **Siegle & Lames, *Game interruptions in elite soccer*** — J. Sports Sci. 30(7) | 2012 | ~**108 interrupções** por jogo | Âncora de sanidade para o número de `D` no jogo completo |

## Inspiração — como melhorar o descodificador

| Trabalho | Ano | O que aproveitar |
|---|---|---|
| **Filtered Semi-Markov CRF** (arXiv:2311.10786) | 2023 | Segmentação com **durações explícitas** e poda eficiente — alternativa ao Viterbi de custo fixo |
| **Hybrid semi-Markov CRF for Neural Sequence Labeling** (arXiv:1805.03838) | 2018 | Como treinar um modelo de sequência com estados de duração variável |
| **Nonhomogeneous HSMM** (arXiv:2312.xxx) | 2023 | Duração dependente de covariáveis (ex.: minuto, resultado, parte) |
| **SoccerNet-Tracking** (arXiv:2204.06918) | 2022 | Benchmark de tracking em vídeo de futebol; boas práticas de avaliação |
| **Ball Trajectory Inference from Multi-Agent Sports Contexts** (Set Transformer + Bi-LSTM hierárquico) | 2023 | Prever a bola a partir dos jogadores quando ela não é vista |
| **Inferring Player Location in Sports: Multi-Agent Spatial Imputation** (arXiv:2302.04567*) | 2023 | Imputação de posições com GNN — cuidado: não usar para inventar bola |
| **TOTNet: Occlusion-Aware Temporal Tracking** (arXiv:2508.09650) | 2025 | Tracking de bola robusto a oclusão, se formos à visão |
| **DeepBall** (arXiv:1902.07304) | 2019 | Detetor de bola; referência de arquitetura |
| **TranSPORTmer** (arXiv:2410.xxxx) | 2024 | Trajetórias multi-agente holísticas; ideias para features de contexto |
| **Pressing Intensity** (2024-12) e **Neighbor-based Pitch Ownership** (arXiv:2501.05870) | 2024-25 | Como quantificar "quem controla o espaço" — features de apoio, não de posse |
| **ELASTIC: Trajectory-Based Synchronization of Event and Tracking Data** (arXiv:2608.30227) | 2026 | Sincronizar eventos e tracking noutros datasets (necessário para o DFL) |
| **Monte Carlo Pass Search** (arXiv:2606.11120) | 2026 | Dataset com trajetórias 3D da bola; útil para estudar passes, não para posse |
| **socceraction / VAEP** — `ML-KULeuven/socceraction` | — | Como representar ações e valor; dá o vocabulário SPADL |

\* verificar o identificador exato antes de citar no relatório final.

## Contexto — porque é que a etiqueta é estranha

- **Opta** define posse como *sequências de ações da mesma equipa* (≈ % de passes), não tempo. **StatsBomb** e **Wyscout** têm definições próprias. Nenhuma coincide com a nossa GT.
- A nossa GT deriva de **tracking corrigido**, mecanicamente: `D` onde a bola está marcada como morta, senão a equipa que o tracking nomeia. Ou seja: **o alvo é o tracker, não o futebol**.
- Consequência: métricas de "posse" da literatura do futebol (Opta/StatsBomb) **não servem** como referência de validação. Só o GT público e o DFL (que também é tracking, não evento) servem.

## Lacunas na literatura (oportunidades nossas)

1. **Ninguém publicou posse a partir de tracking *não corrigido* com 41 % de bola em falta.** O PathCRF assume tracking de jogadores fiável; o DFL é corrigido.
2. **Ninguém comparou Viterbi de custo fixo vs HSMM com durações aprendidas** nesta tarefa.
3. **Ninguém usou modelos de sequência (TCN/Transformer) sobre features de tracking para posse** — as duas melhores equipas públicas dizem explicitamente que não tentaram.
4. **Bordas de interrupção** são resolvidas por deslocamento constante na literatura aplicada; deteção frame a frame (bola fora, silvo) está por fazer.
