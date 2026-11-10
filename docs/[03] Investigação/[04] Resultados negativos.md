# Resultados negativos

**Estado:** vivo · Nada aqui é para repetir. Cada linha custou tempo a alguém.

| # | Ideia | Resultado | Fonte | Conclusão |
|---|---|---|---|---|
| N1 | **Smart Tagging como prior de equipa** | Concordância com o GT público entre 44 % e 100 % dos frames vivos; fases longas atravessam turnovers | Frame Control | Evidência auxiliar, nunca etiqueta |
| N2 | **Bola do broadcast para tapar lacunas do tático** | Turnovers falsos; bolas aéreas caem em pontos diferentes nas duas câmaras (parallax) | Frame Control | Não usar |
| N3 | **Detetores de bola off-the-shelf no vídeo tático** | Bola com ~4 px; frames perdidos são sobretudo oclusões | Frame Control, Cochinae | Sem detetor afinado, não compensa |
| N4 | **Árvores maiores** (127 folhas, 600 árvores) | 0,606 vs 0,608 no DFL | Frame Control | Sem ganho |
| N5 | **Segunda fase a reler os log-odds ±2 s** | +0,009 no DFL, mas pior concordância no nosso jogo | Frame Control | O modelo aprende as curvas do DFL, que não transferem |
| N6 | **Média de dois conjuntos de modelos semelhantes** | 0,609 vs 0,612 | Frame Control | Erram o mesmo; só vale se forem diversos |
| N7 | **Bola perfeita em jogo (teto teórico)** | +0,03 num jogo | Frame Control | Nem o melhor detetor paga o custo |
| N8 | **Regra do "último controlador"** | Piora | Cochinae | A posse não é memória simples |
| N9 | **Interpolação cega de lacunas longas** | Proibida pela lógica e pelos dados: lacunas = bola fora/morta | `docs/[02] Dados` | Nunca interpolar >1 s sem evidência |
| N10 | **Afinar na janela pública de 5 min** | `smooth125` ganha nos 5 min e perde no jogo completo | `vendor/mtah/EVALUATION.md` | 17 posses não ordenam nada |
| N11 | **Copiar o DFL tal e qual** | O DFL muda de posse 7,8–9×/min vivo; este jogo 4,2× | Frame Control | Precisa de adaptação de convenção/duração |
| N12 | **Confiar no congelamento da bola do DFL** | O DFL congela a bola nas paragens; o modelo aprendeu "bola imóvel = morta" e atrasou inícios 2–3,5 s | Frame Control | Reconstruir a bola nas paragens ao treinar |
| N13 | **Bola fora pela posição crua do tracker** | DFL degradado: 0,403 (conf. 3), 0,421 (25), 0,420 (50) vs 0,443; 18,9k–23,2k frames marcados | `scripts/run_e1.py`, DFL J03WMX, 2026-11-08 | A posição da bola é demasiado ruidosa; sem detetor de fora fiável, não usar |
| N14 | **Separar morto/vivo e dono em dois classificadores** | DFL degradado: 0,411 vs 0,443; macro 0,827 vs 0,835; 246 vs 244 posses | `scripts/run_e1.py`, DFL J03WMX, 2026-11-08 | O GBM único de 3 classes é melhor; não separar sem ganho medido |
| N15 | **p90 da velocidade coletiva como feature do GBM** | DFL degradado: 0,428 vs 0,443; macro 0,833 vs 0,835 | `scripts/run_e1.py`, DFL J03WMX, 2026-11-08 | O modelo já tinha `still`/`mean_speed`; o p90 diluiu, não ajudou |
| N16 | **Viterbi de 4 estados + classificador de quem recomeça** | DFL degradado: 0,435 vs 0,443; macro 0,835 vs 0,835; 251 vs 244 posses | `scripts/run_e1.py`, DFL J03WMX, 2026-11-08 | O restart classifier simplificado não pagou; o Frame Control tem um pipeline mais rico |
| N17 | **Etapa física de bola morta (p90/OOB/gap/isolamento, limiares Suleyman)** | DFL degradado: 0,396 vs 0,443; alive/dead F1 0,914 vs 0,948; 36 287 frames mortos | `scripts/run_e1.py`, DFL J03WMX, 2026-11-08 | Os limiares públicos do Suleyman não transferem para o tracker corrigido do DFL; não usar sem calibrar em dados externos |

> **N13 não invalida o refinamento de bordas em geral.** Invalida a regra crua de posição. Os líderes usam p90 da velocidade coletiva, strike do set piece, last-touch (SALT 2025) e snap ao contacto; ver [06] Métodos 2026-11-08.

## Metodologia que já se provou errada

- **Otimizar `accuracy` por frame.** Uma submissão constante numa classe pontua "bem" em acurácia e ~0 em `spellF1`.
- **Avaliar com os 5 minutos.** ±0,06 por posse.
- **Contar posses sem comparar com ~108 paragens/jogo.** Um sistema que produz 669 posses (baseline `smooth50`, medida em 2026-10-25) está a inventar.

## Como acrescentar

Cada negativo novo entra com: ideia, resultado numérico, fonte, e a **decisão** que provocou. Sem número e sem fonte, não entra.
