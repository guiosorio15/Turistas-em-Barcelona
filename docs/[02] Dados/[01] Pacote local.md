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

## Estado da receção do pacote

| Data | Estado | Detalhe |
|---|---|---|
| 2026-10-24 | pacote inicial incompleto | só `tactical/BAR-ATH_tactical_smart_tagging.xml` |
| 2026-10-24 21:43 | **download parado a 4,31 GB** | ficheiro temporário `Não confirmado *.crdownload` no `Downloads`; deixou de crescer às 21:43:23. Verificar no browser se está à espera de confirmação ("Manter") ou em pausa |

Comando de verificação quando o pacote estiver descompactado:

```bash
uv run --locked turistas check-data --data-dir "/caminho/dataset"
```

Critério de "tudo lá": os **9** assets listados acima, todos com tamanho > 0. Se faltar algum, `check-data` devolve código 1 e diz qual.

⚠️ Um `BAR-ATH_broadcast-002.mp4` chegou a existir em `Downloads` e já não existe (resta o atalho em `Recent`). Se o pacote atual vier com nomes numerados, normalizar os nomes para o contrato acima — **o código não adivinha nomes**.

