# Dataset local

O pacote inicial inspecionado em 2026-10-24 só contém `tactical/BAR-ATH_tactical_smart_tagging.xml`. O ZIP disponível contém o mesmo ficheiro.
Foi copiado para `data/tactical/`, preservando a origem. Faltam os restantes oito assets.

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
