# Repositórios de referência

**Estado:** vivo · estrelas e metadados verificados em 2026-10-24 via API do GitHub

Antes de usar qualquer um: verificar **licença** e se os dados que precisa são redistribuíveis. Nada de meter dados do jogo em dependências que os enviem para fora.

## Ferramentas (usar, não reescrever)

| Repositório | ★ | Licença / nota | Para quê |
|---|---|---|---|
| `PySport/kloppy` | 567 | — | Ler ATD (EPTS FIFA), Sportec/DFL, SportsCode. **Ponto de entrada para tudo** |
| `metrica-sports/sample-data` | 503 | dados abertos | 3 jogos com tracking; 1 e 2 com eventos sincronizados → validação extra |
| `andrewRowlinson/mplsoccer` | 551 | MIT | Visualizar campo, trajetórias, mapas de calor (depuração) |
| `ML-KULeuven/socceraction` | 822 | MIT | SPADL, VAEP, xT — vocabulário de ações |
| `probberechts/soccerdata` | 2 121 | — | Scraping (FBref, Sofascore…). **Não usar para este jogo** (dados humanos de terceiros = proibido) |
| `roboflow/supervision` | 51 344 | MIT | Utilitários de CV (anotação, tracking, zonas) |
| `FoundationVision/ByteTrack` | 6 763 | MIT | Tracking multi-objeto |
| `tryolabs/norfair` | 2 693 | MIT | Tracking leve; bom para bola (poucos objetos) |

## Visão computacional de futebol

| Repositório | ★ | O que tem | O que aproveitar |
|---|---|---|---|
| `SoccerNet/sn-gamestate` | 468 | Reconstrução de estado de jogo: tracking + identificação + **papéis** (jogador/árbitro/guarda-redes) | Ideia para **excluir o árbitro** dos toques; pipeline de identificação |
| `SoccerNet/sn-tracking` | 113 | Devkit de tracking | Métricas e formato de avaliação |
| `SoccerNet/sn-calibration` | 111 | Calibração de câmara | Alternativa/comparação com a homografia dada |
| `tryolabs/soccer-video-analytics` | 309 | Posse por vídeo (YOLO + homografia + cor de equipa) | O blog explica as **duas definições** de posse; código mostra distância métrica e estabilização |
| `Tony-Luna/soccer-video-analytics` | 23 | Reimplementação aberta | Comparar abordagens de deteção de equipa |

## Diretamente no nosso problema

| Repositório | ★ | O que é |
|---|---|---|
| `hyunsungkim-ds/pathcrf` | 25 | Código do PathCRF (KDD 2026). Posse sem bola, grafo + CRF + Viterbi. Treina no DFL |
| `danieltyukov/more-than-a-hack-2027` | 0 | **Concorrente**: GBM + Viterbi + degradação do DFL. 0,610 em held-out |
| `dulongski/cochinae-mtah-2027` | 0 | **Concorrente**: forma auto-supervisionada + Viterbi + paper com negativos |
| `reinhart07/mtah-2027-ball-possession` | 0 | **Concorrente**: Viterbi em dois estágios |

## Como usar a concorrência sem violar nada

- Ler é permitido (é público e inspecionável). Copiar sem atribuição é má prática e não nos dá vantagem.
- **Regra interna:** nenhuma linha copiada para `src/turistas/`. Ideias, sim; código, reimplementamos. Se copiarmos algo, fica com atribuição explícita e licença compatível.
- O que interessa reter: **os números** (para saber o que é bom) e **os negativos** (para não gastar tempo).
