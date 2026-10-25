# Turistas de la Nave

**Encontrar quem controla a bola, mesmo quando ela desaparece.**

Equipa de cinco elementos no **More Than a Hack 2027 — Fase 1: Ball Possession**.
A missão: transformar tracking imperfeito e contexto tático em sequências coerentes de posse de bola.

> Estado: estrutura e ambiente preparados; baseline oficial integrada. Modelo próprio por desenvolver. Dataset local incompleto.

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
