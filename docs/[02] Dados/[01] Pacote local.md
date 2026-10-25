# Dataset local

O pacote inicial inspecionado em 2026-10-24 só continha `tactical/BAR-ATH_tactical_smart_tagging.xml`. O download das restantes partes terminou depois; em 2026-10-25 os **9 assets** foram montados em `data/` a partir dos ZIPs `003`–`010` e dos dois MP4 em `~/Downloads`.
Os dois MP4 foram copiados para `data/` a partir de `~/Downloads` (`BAR-ATH_tactical-002.mp4` → `BAR-ATH_tactical.mp4`; `BAR-ATH_broadcast-001.mp4` → `BAR-ATH_broadcast.mp4`), e os restantes ficheiros foram extraídos dos ZIPs. `data/` está no `.gitignore`: nada disto entra no Git.

```text
data/
  tactical/
    BAR-ATH_tactical.mp4
    BAR-ATH_tactical_atd.xml
    BAR-ATH_tactical_atd.txt
    BAR-ATH_tactical_homography.csv
    BAR-ATH_tactical_smart_tagging.xml
  broadcast/
    BAR-ATH_broadcast.mp4
    BAR-ATH_broadcast_atd.xml
    BAR-ATH_broadcast_atd.txt
    BAR-ATH_broadcast_homography.csv
```

`turistas check-data` verifica o pacote completo; `--baseline-only` verifica apenas os dois ficheiros de tracking tático necessários à baseline.
O verificador confirma presença e tamanho não nulo; não certifica integridade ou formatos dos assets.
A baseline usa tracking tático. A câmara broadcast é opcional para a abordagem e tem uma timeline diferente.
Nunca usar caminhos absolutos pessoais em código; passar `--data-dir` ou `MTAH_DATA_DIR`.
Não publicar assets nem derivados que permitam reconstruí-los. Não enviar para serviços de IA alojados.

## Estado da receção do pacote

| Data | Estado | Detalhe |
|---|---|---|
| 2026-10-24 | pacote inicial incompleto | só `tactical/BAR-ATH_tactical_smart_tagging.xml` |
| 2026-10-24 21:43 | download parado a 4,31 GB | registo histórico; o download foi retomado e concluído depois |
| 2026-10-25 | **pacote completo e verificado** | 9/9 assets em `data/`; `check-data` OK; vídeo tático com 199 319 frames a 25 fps |

Comando de verificação:

```bash
uv run --locked turistas check-data --data-dir "/caminho/dataset"
```

Critério de "tudo lá": os **9** assets listados acima, todos com tamanho > 0. Se faltar algum, `check-data` devolve código 1 e diz qual.

⚠️ Os MP4 vieram com nomes numerados (`-001`, `-002`) e foram normalizados ao copiar para o contrato acima. **O código não adivinha nomes.**

## E0 — baseline real (2026-10-25)

```bash
uv run --locked turistas check-data
uv run --locked turistas reproduce
uv run --locked turistas validate outputs/submissions/Turistas_de_la_Nave.csv
uv run --locked turistas evaluate --results outputs/submissions --out outputs/evaluation/submission --bootstrap 1000
```

Resultado: 199 319 linhas; **669 posses**; 7,6 s de duração média; 35,9% `D`; `spellF1` público **0,3256** (IC bootstrap 0,214–0,447); `macroF1` **0,6207**. O CSV é byte-a-byte igual a `vendor/mtah/evaluation/results/baseline_smooth50.csv` (`sha256 6d4e04b8...`). Isto valida a pipeline, não o modelo.

