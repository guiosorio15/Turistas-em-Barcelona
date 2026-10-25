# Calendário e entrega

**Estado:** vivo · **Fonte:** `vendor/mtah/OVERVIEW.md`, `vendor/mtah/SUBMISSION.md`

## Datas publicadas

| Marco | Data | Nota |
|---|---|---|
| Abertura de inscrições | 2026-10-01 | — |
| Libertação dos dados | 2026-10-20 | após enrollment + termos |
| **Entrega** | **2026-11-17** | hora e fuso por confirmar (`?`) |
| Resultados | antes de 2026-11-26 | — |

Ver [05] Perguntas abertas — item "hora-limite e fuso".

## O que se entrega (um formulário)

1. **Ficheiro de posse** — `frame,label`, exatamente **199 319 linhas** (frames 0–199318). É o que é pontuado.
2. **Repositório público** — código, dependências fixadas e **o comando** que regenera o CSV a partir dos dados fornecidos.
3. **Documento técnico** — poucas páginas: abordagem e porquê; que assets foram usados e quais foram descartados; como tratámos lacunas e ruído; que regras de posse implementámos; limitações; como reproduzir.

## Contrato do CSV

- Colunas `frame,label`; `frame` inteiro, 0…199318, por ordem, sem duplicados.
- Labels em `{H, A, D, X}`; célula vazia é **erro** (para abster, escrever `X`).
- Qualquer coisa fora do contrato é rejeitada pelo validador oficial.

Comando de verificação: `uv run --locked turistas validate <ficheiro.csv>`.

## Reprodutibilidade (não é opcional)

Os organizadores podem **re-correr o repositório da equipa vencedora** para confirmar que o ficheiro submetido é o que sai do código. Um resultado que não se reproduz não é um resultado.

Por isso: dependências fixadas (`uv.lock`), modelo treinado versionado ou treino determinístico, e manifesto com hashes de inputs, código e CSV (já implementado em `turistas reproduce`).

## Equipa

3 a 5 elementos. Abaixo de 3 não há elegibilidade para a Innovation Challenge nem para o pitch final. Somos 5 (`docs/[06] Registo/[03] Equipa.md`).
