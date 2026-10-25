# Features

**Estado:** rascunho · a implementar em `src/turistas/`

Regra: **sem identidades**. O ATD não tem IDs de jogador — 46 slots para 22 pessoas. Toda a feature tem de ser coletiva ou relativa ao slot, nunca "o jogador 7".

Tudo em **metros** (multiplicar as coordenadas 0–1 por 105,3 × 68,0) e com o sentido de ataque normalizado por parte.

## 1. Em torno da bola

| Feature | Definição |
|---|---|
| `d1_H`, `d1_A` | distância do jogador mais próximo de cada equipa à bola |
| `d2_H`, `d2_A` | segunda menor distância de cada equipa |
| `n_H_2m`, `n_A_2m`, `n_H_5m`, `n_A_5m` | nº de jogadores de cada equipa a <2 m e <5 m da bola |
| `v_bola`, `a_bola`, `ang_viragem` | velocidade, aceleração e variação de direção da bola (suavizadas) |
| `v_rel_H`, `v_rel_A` | velocidade da bola relativa ao jogador mais próximo de cada lado |

## 2. Para onde a bola vai (a ideia de Link & Hoernig)

| Feature | Definição |
|---|---|
| `proj_0.5_H/A`, `proj_1.0_H/A` | distância do jogador mais próximo de cada equipa à posição prevista da bola a 0,5 s e 1,0 s (velocidade constante) |
| `atras_H`, `atras_A` | quanto o jogador mais próximo está "atrás" da linha da bola (sinal de quem a pode intercetar) |

## 3. Visibilidade da bola

| Feature | Definição |
|---|---|
| `frames_desde_vista`, `frames_ate_vista` | distância temporal à última/próxima observação |
| `visto_1s`, `visto_4s` | fração de frames com bola na janela ±1 s e ±4 s |
| `gap_len` | duração da lacuna em que o frame cai |

> Estas features são o que permite ao modelo **distinguir "bola morta" de "bola ocluída em jogo"** — a distinção que a baseline não faz.

## 4. Forma da equipa (a que salva os frames sem bola)

Por equipa, no seu sentido de ataque:

- `centroide_x/y`, `dispersão`, `profundidade` (quantis 10/50/90), `largura`, `última linha`
- `velocidade_para_a_frente`, `velocidade_média`, `pressão` (nº de adversários a <10 m de cada jogador)
- **tendências** a ±0,5 s e ±2 s das mesmas grandezas

Sozinhas, identificaram corretamente o lado em posse em **83 % dos frames vivos** da janela pública (medição da Frame Control) — sem ver a bola.

## 5. Histórico de controlo (histerese)

| Feature | Definição |
|---|---|
| `frames_desde_controlo_H/A` | frames desde que cada equipa teve controlo claro (bola a <1 m, adversário mais próximo a >2,5 m, bola <6 m/s) |
| `equilíbrio_0.25/1/3s` | média de "quem está mais perto" nas janelas anteriores e posteriores |
| `mudanca_de_lado_recente` | quantas vezes a evidência trocou de lado nos últimos 2 s |

## 6. Contexto de interrupção

| Feature | Definição |
|---|---|
| `tag_setpiece_ativa` | está dentro de um `SET PIECES` do Smart Tagging |
| `tag_tipo` | throw-in / corner / goal kick / free kick / kick-off (one-hot) |
| `tag_team_missing` | 1 se `Team = N/A` (todos os throw-ins) |
| `broadcast_sem_campo` | fração do segundo em torno do frame sem vista de campo no broadcast |
| `parado_ha` | frames desde que a bola deixou de se mover e a equipa parou |

## 7. O que **não** entra

- Identidade de jogador (não existe).
- Coordenadas de pixel cruas (usar homografia só para visão).
- Qualquer constante escolhida a olhar para frames específicos deste jogo.

## Nota de implementação

Uma função, um DataFrame, mesma assinatura para o jogo-alvo e para o DFL. É isso que torna a degradação e a validação possíveis — e é onde os projetos falham.
