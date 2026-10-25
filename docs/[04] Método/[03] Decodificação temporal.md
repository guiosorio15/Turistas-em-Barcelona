# Decodificação temporal

**Estado:** rascunho

O classificador diz "neste frame, 0,62 para H". A métrica não pontua isso: pontua **posses inteiras**. Este documento é sobre a passagem de probabilidades a intervalos.

## Porque é que isto decide o resultado

- Um classificador a 90 % por frame que alterna de label a cada 2 frames cria **centenas de posses falsas** e pontua perto de 0.
- Uma posse recuperada na perfeição mas **1 s atrasada** vale ~0,65.
- A baseline `smooth50` ilustra: 594 posses previstas num jogo com ~108 paragens.

## Formulação

Estados ocultos: `H`, `A`, `D_H` (bola morta, casa recomeça), `D_A` (bola morta, fora recomeça).

- `D_H`/`D_A` existem para que **quem está sobre a bola durante a paragem** (o lançador, o canto, o guarda-redes) decida o recomeço, em vez do que acontece no primeiro segundo depois.
- `D` só pode terminar no lado que reinicia. Isso remove transições impossíveis.

### Custo fixo (Viterbi) — o ponto de partida

```
score(caminho) = Σ log P(estado | features) − Σ custo(transição)
custo: turnover = 9 · entrar/sair de paragem = 12 · mudar de quem recomeça = 1
```

Custos vindos da literatura aplicada; **não** afinados no jogo. O custo de turnover controla diretamente quantas posses o sistema inventa — é o parâmetro mais sensível ao domínio.

### Durações explícitas (HSMM) — a nossa aposta

O custo fixo assume que todas as posses duram o mesmo. Não duram. Um HSMM modela `P(duração = d | estado)`, estimada em **outros jogos**:

```
score = Σ log P(estado | features) + Σ log P(duração) − custo de mudança
```

Vantagens: posses curtas legítimas (0,8 s) deixam de ser "caras", e posses longas deixam de ser penalizadas. E o parâmetro passa a ser **uma distribuição aprendida**, não um número escolhido à mão — o que também é mais defensável perante as regras.

## Restrições duras (não negociáveis)

1. **Duração mínima de paragem** (ex.: 0,4 s) — evita `D` de 3 frames.
2. **Duração mínima de posse** (ex.: 0,4 s) — mas não eliminar posses curtas reais.
3. **Bordas:** o início da paragem tende a ser **antes** do que os jogadores reagem (a bola desaparece no instante em que sai). Corrigir com evidência (bola fora do polígono, silvo), não com deslocamento constante.
4. **Frames não avaliados** (pré-jogo, intervalo, após o fim): escrever `X` — custa 0.

## Refinamento de bordas (o detalhe que ninguém fez)

Por ordem de custo/benefício:

| Sinal | Como | Confiança |
|---|---|---|
| Bola cruza a linha lateral/fundo | posição + velocidade; extrapolar 0,2 s | alta |
| Bola para de se mover + jogadores abrandam | velocidade da bola e média das equipas | média |
| `SET PIECES` do Smart Tagging | intervalo conhecido do recomeço | média (N/A nos throw-ins) |
| Broadcast sem vista de campo | close-up/repetição | alta (com alinhamento) |
| **Silvo** (áudio) | deteção de pico espectral | a confirmar se há faixa áudio |

## Algoritmo (esboço)

```python
def decode(logp, durations, costs):
    # logp: (T, 4) log-probabilidades por frame
    # durations: distribuições de duração por estado (aprendidas fora deste jogo)
    # costs: matriz 4x4 de custo de transição
    return best_path_via_hsmm(logp, durations, costs)  # → labels (T,)
```

Determinismo obrigatório: mesma entrada + mesma config → **mesmo ficheiro** (requisito de entrega).

## Como avaliar o descodificador

Nunca por acurácia por frame. Sempre por `spellF1` em **outros jogos**, mais:
- nº de posses previstas vs ~108 paragens/jogo;
- erro médio de borda em frames;
- distribuição de durações previstas vs real.

Ver [04] Avaliação e protocolo.
