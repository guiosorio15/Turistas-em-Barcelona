# Perguntas abertas aos organizadores

**Estado:** rascunho · Nada aqui está respondido. Perguntar **antes** de construir em cima de qualquer destes pontos.

Formato sugerido: abrir issue no repositório oficial (é o canal que o `RULES.md` indica).

| # | Pergunta | Porque importa | Impacto se "não" |
|---|---|---|---|
| P1 | Podemos usar o repositório público de outra equipa como **referência metodológica**? E copiar código com atribuição? | Há 20+ repos públicos; a regra diz "any method, desde que inspecionável" | Muda a estratégia de I&D |
| P2 | Podemos treinar com **tracking corrigido de outros jogos** (DFL/Sportec, CC-BY 4.0) e com a posse por frame que esse dataset traz? | É a base do nosso protocolo de validação | Ficamos só com auto-supervisão |
| P3 | O **áudio** do vídeo tático (silvo, voz) pode ser usado? | Deteção de interrupções frame a frame | Perdemos o melhor sinal de bordas |
| P4 | Alinhar o **broadcast** ao tático por correlação automática de trajetórias é permitido? | É transformação algorítmica, não anotação | Perdemos o sinal de "a TV cortou para um close-up" |
| P5 | Pseudo-etiquetas geradas por algoritmo **neste** jogo (self-training) contam como anotação? | A regra permite explicitamente; queremos confirmação escrita | Evitamos a técnica |
| P6 | Corrigir o tracking com um **detetor próprio** (ex.: bola em oclusão) é permitido? | `RULES.md` diz que sim; confirmar que não há limite de "frame a frame" | Perdemos o +0,03 estimado |
| P7 | Qual é a **hora-limite e o fuso** de 2026-11-17? | Evita perder a submissão por 1 hora | — |
| P8 | Há **fases seguintes** (Fase 2/pitch)? Com que critérios? | `OVERVIEW.md` sugere que sim, sem detalhar (`?`) | Muda o esforço em documentação |
| P9 | O ranking final usa **só** o jogo completo privado, ou também os 5 min? | `OVERVIEW.md` diz jogo completo; confirmar | — |
| P10 | Se o repositório for público durante a prova, os organizadores copiam/avaliam submissões de terceiros? | Publicar cedo pode dar vantagem a outros | Estratégia de timing |

## Como registar a resposta

Quando houver resposta, atualizar esta tabela com `P# — respondido em AAAA-MM-DD: <resumo>` e registar a decisão em `docs/[06] Registo/[01] Decisões.md`. Nunca deixar uma resposta só no chat.
