# Trabalhar em equipa

Ler [AGENTS.md](AGENTS.md), o [índice da documentação](docs/[00]%20Índice.md) e a [instalação](docs/[05]%20Operação/[01]%20Instalação.md).
Criar branches `feat/tema`, `fix/tema` ou `docs/tema`. Propor alterações por pull request e pedir revisão a outro elemento.
Manter PRs pequenos; indicar problema, alteração e validação. Não incluir datasets nem resultados locais restritos.
Antes do PR: `uv run --locked python -m unittest discover -s tests -v` e `uv run --locked turistas evaluate`.
Registar decisões em `docs/[06] Registo/[01] Decisões.md` e resultados agregados no relatório, identificando o commit e os parâmetros.
Não comparar variantes para selecionar modelos com base nos cinco minutos públicos.
