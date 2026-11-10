# Turistas de la Nave

**Encontrar quem controla a bola, mesmo quando ela desaparece.**

Equipa de cinco elementos no **More Than a Hack 2027 — Fase 1: Ball Possession**.
A missão: transformar tracking imperfeito e contexto tático em sequências coerentes de posse de bola.

> Estado: baseline oficial validada com tracking real e primeiro modelo próprio (E2) treinado em 7 jogos DFL; LOMO concluído em 0,525 ± 0,037. Os labels e o score da baseline são iguais ao oficial; neste Windows o hash difere só por CRLF vs LF. E5/E2b/E5b testados e negativos; E2 congelado.

## Arrancar em minutos

Instala [Git](https://git-scm.com/) e [uv](https://docs.astral.sh/uv/getting-started/installation/).
Clona o repositório da equipa (é necessário acesso ao repositório privado):

```bash
git clone git@github.com:guiosorio15/Turistas-em-Barcelona.git
cd Turistas-em-Barcelona
uv sync --locked
uv run --locked turistas check-data
uv run --locked turistas evaluate
uv run --locked python -m unittest discover -s tests -v
```

`check-data` devolve erro enquanto faltarem assets. A avaliação das quatro baselines incluídas funciona sem dataset.
O `uv` instala o Python 3.11 e as versões fixadas em `uv.lock`.
[Guia completo para Linux, macOS e Windows](docs/[05]%20Operação/[01]%20Instalação.md). [Verificações e limites](docs/[05]%20Operação/[03]%20Verificação%20e%20CI.md).

## Com os dados autorizados

Descarrega o pacote completo através do acesso dos organizadores. Coloca as pastas `tactical/` e `broadcast/` em `data/`, ou indica a localização:

```bash
uv run --locked turistas check-data --data-dir "/caminho/para/dataset"
uv run --locked turistas reproduce --data-dir "/caminho/para/dataset"
uv run --locked turistas validate outputs/submissions/Turistas_de_la_Nave.csv
uv run --locked turistas evaluate --results outputs/submissions
```

A reprodução gera a baseline `smooth50`, o CSV da equipa e um manifesto com hashes, versão do código e parâmetros. **É um ponto de partida, não uma solução melhorada.**
Neste checkout, com os assets de tracking locais, a baseline real foi reproduzida: `spellF1` público 0,3256, `macroF1` 0,6207 e 669 posses no jogo completo. Os labels e o score são iguais ao oficial; em Windows o hash difere apenas por CRLF vs LF.
Dados, resultados e relatórios gerados ficam locais. Nunca adicionar os dados restritos ao Git.

## Modelo próprio (E2)

Pipeline: features coletivas sem identidades → GBM de 3 classes → Viterbi de 3 estados. Treino e afinação só em 7 jogos DFL/Sportec (CC-BY 4.0), com degradação do tracking (41% bola em falta, lacunas longas, jogadores em falta, ruído). O jogo fornecido entra apenas como input; o GT público serve só para contrato e sanidade.

| Medição | Resultado |
|---|---|
| DFL degradado, split período 1→2 no J03WMX | `spellF1` **0,443** (244 posses previstas vs 261) |
| Jogo completo, modelo dos 7 jogos | 43,1% `D`; 415 posses; 8,7 s |
| Público isolado, modelo dos 7 jogos | `spellF1` 0,5455; 27 posses; ±0,25 — **não é seleção** |
| LOMO 7 jogos | **0,525 ± 0,037** (macro 0,868) |

Comando de inferência:

```bash
uv run --locked python scripts/predict_target.py \
  --model models/e1_dfl_v3.joblib \
  --output outputs/submissions/Turistas_de_la_Nave.csv
```

A regra de bola fora, os três classificadores e os componentes do E5b (4 estados, p90, etapa física) foram testados em DFL e pioraram; o E2 está congelado. E4/HSMM fica adiado sem um prior externo adequado; E6 (TCN + SkillCorner) é o caminho restante.

Treino reproduzível: `uv sync --locked --extra notebooks`, `uv run --locked python scripts/fetch_dfl.py`, `uv run --locked --extra notebooks python scripts/train_model.py`.

## O desafio

| Aspeto | Contrato |
| --- | --- |
| Jogo | FC Barcelona–Athletic Club |
| Saída | `frame,label`, 199 319 linhas de dados, frames 0–199318 |
| Estados | `H`: casa; `A`: visitante; `D`: bola parada; `X`: abstenção |
| Classificação | `spellF1`; primeiro desempate por `macroF1` |
| Referência publicada | `spellF1` 0,2433 no jogo completo, baseline `smooth50` |
| Entrega | CSV + repositório público reproduzível + documento técnico |
| Prazo publicado | 2026-11-17 |

Fonte: [repositório oficial](https://github.com/metrica-sports/more-than-a-hack-2027).
Os cinco minutos públicos verificam o funcionamento; não são dados de treino nem de afinação.

## Encontrar cada coisa

```text
src/turistas/       CLI e implementação da equipa
configs/            parâmetros versionados
models/             artefacto do modelo próprio (treinado em DFL público)
scripts/            aquisição DFL, treino e inferência
vendor/mtah/        referência oficial preservada, incluindo scorer e baselines
notebooks/          exploração; lógica reutilizável fica em src/
docs/[00] Índice.md portal da documentação (começar aqui)
docs/[01] Competição/ regras, métricas, calendário e perguntas abertas
docs/[02] Dados/      inventário, ATD, Smart Tagging, homografia e broadcast
docs/[03] Investigação/ papers, repositórios, concorrência e resultados negativos
docs/[04] Método/     arquitetura, features, decodificação, avaliação e experimentos
docs/[05] Operação/   instalação, comandos e verificação
docs/[06] Registo/    decisões, diário, equipa e plano de trabalho
docs/[99] Arquivo/    notas originais da equipa e imagens
data/               assets autorizados, locais
outputs/            submissões e relatórios gerados, locais
tests/              verificações da integração
```

## Começar a contribuir

1. Abrir o [índice da documentação](docs/[00]%20Índice.md).
2. Ler a [visão geral](docs/[01]%20Competição/[01]%20Visão%20geral.md) e as [ideias](docs/[03]%20Investigação/[05]%20Ideias.md).
3. Perceber o que já falhou em [resultados negativos](docs/[03]%20Investigação/[04]%20Resultados%20negativos.md).
4. Escolher uma frente no [plano de trabalho](docs/[06]%20Registo/[04]%20Plano%20de%20trabalho.md) e na [equipa](docs/[06]%20Registo/[03]%20Equipa.md).
5. Consultar [CONTRIBUTING.md](CONTRIBUTING.md) e [AGENTS.md](AGENTS.md).

Código oficial sob licença MIT em `vendor/mtah/LICENSE`. A licença do código da equipa ainda está por decidir. O dataset tem termos separados e não é redistribuível.
Repositório da equipa: [guiosorio15/Turistas-em-Barcelona](https://github.com/guiosorio15/Turistas-em-Barcelona), privado durante o desenvolvimento. A entrega exige torná-lo público. O commit inicial criado no GitHub foi preservado no histórico.
