# Turistas de la Nave — relatório técnico

**Estado: rascunho. Não representa uma solução final.**

## Abordagem implementada
Integração da baseline oficial por proximidade do jogador à bola e votação temporal `smooth50` (meia janela de 50 frames). Nenhum modelo próprio foi ainda implementado.

## Dados utilizados
A baseline usa tracking tático automático e respetivos metadados. Smart Tagging, vídeo e homografia não são usados por esta baseline.
Dados de treino anotados utilizados pela equipa: nenhum nesta versão.

## Posse, ruído e lacunas
O comportamento atual é o da baseline oficial; não implementa ainda todas as regras de controlo discutidas nas ideias. Descrever alterações aqui quando existirem.

## Resultados
Avaliação das baselines incluídas: ver `outputs/evaluation/scoreboard.csv` após execução.
Resultado do modelo próprio: `?`.
Reprodução a partir do tracking real: pendente de dados.
Não confundir scores públicos com os resultados privados publicados pelos organizadores.

## Reprodução
`uv sync --locked`, seguido de `uv run --locked turistas reproduce --data-dir "/caminho/dataset"`.
Validar com `uv run --locked turistas validate outputs/submissions/Turistas_de_la_Nave.csv`.
A execução guarda manifesto local com hashes e parâmetros. Para a entrega final, identificar commit, dependências, limitações e comando exato.

## Limitações e entrega
Dataset inicial incompleto; pipeline real ainda não executada. Teste noutro sistema operativo e clone remoto por fazer.
Entregar CSV e este relatório finalizado com o nome da equipa, mais URL público do código, conforme `vendor/mtah/SUBMISSION.md`.
