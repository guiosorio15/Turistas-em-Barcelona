# Smart Tagging

**Estado:** vivo · **Fonte:** `vendor/mtah/DATA.md` §Smart Tagging

Anotação **automática** de fases táticas (não revista por humanos). 638 instâncias, em XML de SportsCode.

## Como ler

```python
from kloppy import sportscode
events = sportscode.load(asset_paths()["smart_tagging"]).to_df()
```

Ou sem kloppy: `vendor/mtah/starter/load_smart_tagging.py` (só biblioteca padrão).

- Códigos em MAIÚSCULAS (`SET PIECES`); valores das tags em Title Case (`Kick Off (Start)`).
- Colunas de tag: `Team`, `Half`, `Type`, `Side`, `Direction of ball entry`, `Max Players in the box`.
- **Base temporal:** `<start>`/`<end>` em **segundos desde o primeiro frame do vídeo tático**; `frame = round(segundos × 25)`. Verificado contra os dois pontapés de saída.

## Inventário (638)

| Código | n | Código | n |
|---|---|---|---|
| `PLAYERS IN THE BOX` | 97 | `CREATING CHANCES` | 30 |
| `BALL IN FINAL THIRD` | 93 | `DEFENDING IN DEFENSIVE THIRD` | 30 |
| `BALL IN THE BOX` | 72 | `LONG BALL` | 29 |
| `PROGRESSION` | 66 | `ATTACKING TRANSITION` | 24 |
| `DEFENDING IN MIDDLE THIRD` | 66 | `DEFENSIVE TRANSITION` | 24 |
| `SET PIECES` | 59 | `BUILD UP` | 22 |
| | | `DEFENDING IN ATTACKING THIRD` | 22 |
| | | `GOALS` | 4 |

`Team`: Barcelona 314 · Atletic Club 288 · **N/A 36** (inclui **todos** os throw-ins).
`Type`: Throw-in 26 · Corner 12 · Goal Kick 10 · Free Kick 5 · Kick Off (After Goal) 4 · Kick Off (Start) 2.

## O que vale e o que não vale

**Vale:**
- Cada set piece é um recomeço → a interrupção anterior terminou ali.
- Cada fase tem uma equipa → prior fraco de posse.

**Não vale:**
- **Não é verdade.** Falsos positivos e negativos, sem revisão humana.
- **`Team = N/A` em 36 casos**, precisamente em todos os throw-ins — onde saber o lado valia mais.
- **Fases ≠ posses.** Um Build Up pode cobrir uma posse, ficar a meio ou atravessar duas.
- A concordância por código com o GT público varia entre **44 % e 100 %** dos frames vivos, e as fases longas ("final third", "box") atravessam turnovers (medição da equipa Frame Control).

## Decisão atual

Usar **apenas** como: (a) evidência auxiliar de interrupção e recomeço; (b) verificação de sanidade no jogo completo (nº de paragens, concordância de fase). **Não** usar como etiqueta, nem como input principal de um classificador — ver `docs/[03] Investigação/[04] Resultados negativos.md`.
