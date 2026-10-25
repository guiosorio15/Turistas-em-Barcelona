# Comandos

Executar na raiz, após `uv sync --locked`.

| Comando (prefixo `uv run --locked`) | Função |
| --- | --- |
| `turistas check-data` | Listar assets presentes e em falta; código de saída 1 se incompleto |
| `turistas check-data --baseline-only` | Verificar tracking tático mínimo |
| `turistas evaluate` | Avaliar as quatro baselines oficiais sem dataset |
| `turistas reproduce --data-dir "/caminho/dataset"` | Gerar baseline da equipa, validar e guardar manifesto |
| `turistas validate outputs/submissions/Turistas_de_la_Nave.csv` | Verificar o contrato oficial |
| `turistas evaluate --results outputs/submissions` | Avaliar a submissão nos cinco minutos públicos |
| `python -m unittest discover -s tests -v` | Executar testes da integração |

`reproduce --config configs/baseline.toml` escolhe parâmetros versionados. `--output-dir` escolhe a pasta de submissões.
`evaluate --out outputs/evaluation` escolhe onde guardar os relatórios; `--bootstrap 1000` ativa intervalos de confiança.
Não usar o resultado público para selecionar modelos ou afinar parâmetros.
