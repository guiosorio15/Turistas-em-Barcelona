# Concorrência pública

**Estado:** vivo · levantamento de 2026-10-24 · **fonte:** pesquisa na API do GitHub (`gh search repos`)

## O facto que define a estratégia

O repositório oficial tem **129 ★** e, em 24 de outubro, existiam **mais de 20 repositórios de equipas** públicos, alguns com código, modelos treinados e paper. Não estamos sozinhos e as boas ideias já circulam.

**Portanto:** ganhar não vai ser "ter a ideia". Vai ser **executar melhor** — protocolo de validação honesto, robustez ao domínio e detalhe nas bordas.

## Os três que importam

### 1. Frame Control — `danieltyukov/more-than-a-hack-2027`

| | |
|---|---|
| Abordagem | Features sem identidades + 3 `HistGradientBoosting` (bola morta / dono / quem recomeça) + **Viterbi de 4 estados** + broadcast como sinal de bola morta |
| Treino | **7 jogos DFL/Sportec degradados** para imitar o nosso tracker (lacunas de 3–30 s, bolas aéreas projetadas no relógio, jogadores a desaparecer, ruído) |
| Resultado | **0,610 `spellF1`** em leave-one-match-out nos 7 jogos DFL (~3 000 posses) · 0,650 nos 5 min públicos · macroF1 0,914 |
| Jogo completo | 293 posses previstas, 50 % de frames mortos, 120 paragens |

**O que aprender:** a ideia da **degradação** (treinar no limpo, testar no sujo) é o truque central e é reproduzível. E a validação honesta em 7 jogos é o que nos falta.

**O que não copiar:** ajustaram **4 pesos de broadcast + 1 deslocamento temporal** nos 5 minutos públicos. É afinação na janela proibida e um risco de desqualificação.

### 2. Cochinae — `dulongski/cochinae-mtah-2027`

| | |
|---|---|
| Abordagem | Classificador de **forma da equipa auto-supervisionado** (proxy labels quando a bola está a 1,5 m de um jogador) + proximidade da bola + modelo físico de bola morta + Viterbi com duração mínima + **self-training** |
| Resultado | 0,542 público · macroF1 0,867 |
| Extra | Paper com **resultados negativos** explícitos |

**O que aprender:** auto-supervisão **no próprio jogo** é permitida e evita depender do DFL. Erros descorrelacionados dos do Frame Control → candidato natural a **ensemble**.

### 3. Rei JR — `reinhart07/mtah-2027-ball-possession`

Viterbi em dois estágios, determinístico, ~3 min. Menos documentado publicamente; útil como terceira opinião sobre o descodificador.

## Outros (para varrer, não para ler tudo)

`scoreadvise`, `darfattt`, `kovidhpathakk`, `SYEDMDSAAD` (Mes Que Un Club), `KAsare1` (Team Asare), `NaufalFahrozi`, `Mar3eczek17`, `HellThrall2000`, `2dhammahmoud`, `maxoubvd`, `ikhsansdqq`, `Bryne77`, `dabidu27`, `f-gonzo`, `alx-du`, `NEXE-sudo`, `hassaangatta`, `Joanfmir` (cópia do oficial).

## Escala de referência (para não nos enganarmos)

| Sistema | `spellF1` público | `spellF1` jogo completo |
|---|---|---|
| Baseline oficial `smooth50` | 0,326 | **0,2433** |
| Baseline oficial `smooth125` | 0,424 | 0,2242 |
| Cochinae | 0,542 | `?` |
| Rei JR | `?` | `?` |
| Frame Control | **0,650** | `?` (0,610 em DFL held-out) |

⚠️ **A coluna pública não ordena sistemas:** 17 posses, ±0,06 por posse. Só a coluna DFL (`leave-one-match-out`) é comparável.

## Leitura estratégica

1. **Todos convergem** em: features geométricas → classificador → Viterbi. O que difere é o treino (DFL vs auto-supervisão) e o refinamento.
2. **Ninguém resolveu** as bordas de interrupção, as posses curtas (<1,5 s) nem usou modelos de sequência.
3. **O código público é assimétrico:** quem publica cedo perde vantagem; quem publica bem ganha reputação. Nós devemos manter o repo privado até à entrega (o `RULES.md` exige público **na entrega**).
