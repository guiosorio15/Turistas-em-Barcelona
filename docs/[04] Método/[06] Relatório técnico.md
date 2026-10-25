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
Avaliação das baselines incluídas: ver `outputs/evaluation/scoreboard.csv`.
Resultado do modelo próprio: `?`.
Reprodução a partir do tracking real: **concluída em 2026-10-25**. 199 319 linhas, **669 posses**, 7,6 s de duração média, 35,9% `D`; `spellF1` público **0,3256** (IC bootstrap 0,214–0,447), `macroF1` **0,6207**. O CSV é byte-a-byte igual a `baseline_smooth50` oficial (`sha256 6d4e04b8...`).
Não confundir scores públicos com os resultados privados publicados pelos organizadores.

## Reprodução
`uv sync --locked`, seguido de `uv run --locked turistas reproduce --data-dir "/caminho/dataset"`.
Validar com `uv run --locked turistas validate outputs/submissions/Turistas_de_la_Nave.csv`.
A execução guarda manifesto local com hashes e parâmetros. Para a entrega final, identificar commit, dependências, limitações e comando exato.

## Limitações e entrega
Dataset completo montado localmente (9/9 assets); pipeline real executada e validada. O modelo próprio ainda não existe. Clone local independente validado em Linux, incluindo ambiente limpo, seis testes e avaliação pública. Testes noutros sistemas operativos e CI remota por confirmar.
Entregar CSV e este relatório finalizado com o nome da equipa, mais URL público do código, conforme `vendor/mtah/SUBMISSION.md`.
