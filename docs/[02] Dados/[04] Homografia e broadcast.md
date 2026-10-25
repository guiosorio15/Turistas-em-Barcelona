# Homografia e broadcast

**Estado:** vivo · **Fonte:** `vendor/mtah/DATA.md` §§Homography, The broadcast recording

## Homografia

Uma matriz **3×3 por frame** que leva coordenadas normalizadas do campo (0–1, a mesma convenção do ATD) a píxeis da imagem.

```
frame,h00..h22,reprojection_error,valid
11185,1822.663,...,0.2910854,1
```

- `valid = 0` → as 9 colunas da matriz são `NaN`; **não há transformação** nesse frame.
- `reprojection_error` → quanto a matriz erra (menor é melhor). Tático: mediana 0,24 em jogo, ~1,5 no intervalo. Broadcast: chega a 304.
- Tático: **100 % válida**. Broadcast: **65,8 %** válida, em 122 troços (o maior com mais de 1 min 30 s).

Utilidade para nós: projetar jogadores/bola para o frame e ver o que o tracker "via"; recortar a região da bola para um detetor próprio; decidir se um frame serve para visão.

## Broadcast

- É a emissão de TV: cortes, repetições, zooms, close-ups, bancada.
- **Não está alinhado** ao tático e não há tabela de correspondência.
- ATD próprio (164 488 registos, 51 slots) e homografia própria (65,8 % válida).
- **Se a submissão tiver ~164 mil linhas, indexámos o broadcast** — o validador rejeita. O índice da submissão é sempre o vídeo **tático**.

## Alinhamento (o que se sabe)

A equipa Frame Control encontrou **um offset fixo por parte**, por correlação da trajetória da bola:

```
frame_tático ≈ frame_broadcast + 4014   (1.ª parte)
frame_tático ≈ frame_broadcast + 26920  (2.ª parte)
```

…com correção de deriva de 1–2 frames janela a janela, e marcação de "frame vivo" quando os jogadores do broadcast estão a ≤1,5 m dos do tático. **É uma medição deles, não nossa** — reproduzir antes de usar.

## O sinal mais valioso do broadcast

**O realizador corta para close-up/repetição quando a bola está parada.** Na janela pública deles: 76 % dos frames mortos não mostram campo, contra 3 % dos vivos. Isso levou a precisão de `dead/alive` de 0,875 para 0,952.

⚠️ **Atenção regulamentar:** esses pesos foram ajustados **nos 5 minutos públicos**, o que a regra 2 do `RULES.md` proíbe na prática. Nós queremos o mesmo sinal, mas com pesos justificados por **outros jogos** ou por regra física, não por afinação na janela pública.

## O que NÃO fazer

- **Não** usar a bola do broadcast para preencher lacunas do tático. Tentado e abandonado: bolas aéreas caem em pontos diferentes do relvado nas duas câmaras (parallax) e geram turnovers falsos.
- **Não** assumir que a homografia do broadcast existe no frame — verificar `valid`.
