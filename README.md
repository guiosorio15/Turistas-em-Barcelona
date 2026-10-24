# Turistas de la Nave

**Encontrar quem controla a bola, mesmo quando ela desaparece.**

Equipa de cinco elementos no **More Than a Hack 2027 — Fase 1: Ball Possession**.
A missão: transformar tracking imperfeito e contexto tático em sequências coerentes de posse de bola.

> Estado: estrutura e ambiente preparados; baseline oficial integrada. Modelo próprio por desenvolver. Dataset local incompleto.

## Arrancar em minutos

Instala [Git](https://git-scm.com/) e [uv](https://docs.astral.sh/uv/getting-started/installation/).
Depois de este repositório estar publicado, clona o URL da equipa e entra na pasta clonada.
Enquanto o URL não existir, podes copiar esta pasta para outro computador, incluindo os ficheiros ocultos.

```bash
uv sync --locked
uv run --locked turistas check-data
uv run --locked turistas evaluate
uv run --locked python -m unittest discover -s tests -v
```

`check-data` devolve erro enquanto faltarem assets. A avaliação das quatro baselines incluídas funciona sem dataset.
O `uv` instala o Python 3.11 e as versões fixadas em `uv.lock`.
[Guia completo para Linux, macOS e Windows](docs/ambiente/instalacao.md). [Verificações e limites](docs/ambiente/verificacao.md).

## Com os dados autorizados

Descarrega o pacote completo através do acesso dos organizadores. Coloca as pastas `tactical/` e `broadcast/` em `data/`, ou indica a localização:

```bash
uv run --locked turistas check-data --data-dir "/caminho/para/dataset"
uv run --locked turistas reproduce --data-dir "/caminho/para/dataset"
uv run --locked turistas validate outputs/submissions/Turistas_de_la_Nave.csv
uv run --locked turistas evaluate --results outputs/submissions
```

A reprodução gera a baseline `smooth50`, o CSV da equipa e um manifesto com hashes, versão do código e parâmetros. **É um ponto de partida, não uma solução melhorada.**
Dados, resultados e relatórios gerados ficam locais. Nunca adicionar os dados restritos ao Git.

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
vendor/mtah/        referência oficial preservada, incluindo scorer e baselines
notebooks/          exploração; lógica reutilizável fica em src/
docs/projeto/       visão, equipa, plano, ideias e decisões
docs/tecnica/       arquitetura, dados, avaliação e relatório
docs/ambiente/      instalação, dataset e comandos
docs/referencias/   notas originais da equipa e imagens
data/               assets autorizados, locais
outputs/            submissões e relatórios gerados, locais
tests/              verificações da integração
```

## Começar a contribuir

1. Ler a [visão geral](docs/projeto/visao-geral.md) e as [ideias](docs/projeto/ideias.md).
2. Escolher uma frente no [plano da equipa](docs/projeto/equipa.md).
3. Consultar [CONTRIBUTING.md](CONTRIBUTING.md) e [AGENTS.md](AGENTS.md).

Código oficial sob licença MIT em `vendor/mtah/LICENSE`. A licença do código da equipa ainda está por decidir. O dataset tem termos separados e não é redistribuível.
URL do repositório da equipa: **?** — repositório Git local preparado, ainda sem publicação.
