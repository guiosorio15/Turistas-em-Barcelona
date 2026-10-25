# Dados e alinhamento

A referência da submissão é o vídeo tático: 199 319 frames, 25 fps, índices de 0 a 199318.
`games.py` oficial centraliza caminhos, dimensões do campo e offsets. Não duplicar constantes em módulos próprios.
A relação `id_frame = video_frame + offset` depende da parte: consultar `vendor/mtah/games.py`.
Não aplicar um único offset a todo o jogo nem assumir alinhamento entre broadcast e tactical.
Converter coordenadas normalizadas para metros antes de interpretar distâncias ou velocidades.

Verificar ausências, coordenadas inválidas, saltos e fragmentação de identidades. Não preencher lacunas longas por interpolação cega.
Smart Tagging é automático e pode ter falsos positivos e negativos. Homografias incluem um indicador de validade.

Fontes: [DATA.md oficial](https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md), cópia em `vendor/mtah/DATA.md`.
