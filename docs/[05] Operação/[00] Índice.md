# [00] Índice — Operação

Pôr a máquina a andar e provar que anda.

| # | Documento | Estado |
|---|---|---|
| [01] | [Instalação]([01]%20Instalação.md) — Git, uv, Python, Windows/Linux/macOS | vivo |
| [02] | [Comandos]([02]%20Comandos.md) — a CLI `turistas` | vivo |
| [03] | [Verificação e CI]([03]%20Verificação%20e%20CI.md) — testes e limites conhecidos | vivo |

## O caminho mais curto

```bash
git clone git@github.com:guiosorio15/Turistas-em-Barcelona.git
cd Turistas-em-Barcelona
uv sync --locked
uv run --locked turistas check-data --data-dir "/caminho/dataset"
uv run --locked turistas reproduce --data-dir "/caminho/dataset"
uv run --locked python -m unittest discover -s tests -v
```

## Regra de ouro

Nada é "feito" até correr num clone limpo, noutro computador, com `uv sync --locked`. O relatório só pode citar números que saiam destes comandos.
