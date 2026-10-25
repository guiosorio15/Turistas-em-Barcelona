# Decisões

| Data | Decisão | Motivo |
| --- | --- | --- |
| 2026-10-24 | Separar código próprio e referência oficial | Preservar o scorer e facilitar atualização |
| 2026-10-24 | Python 3.11 e uv com lock | Instalação consistente entre computadores |
| 2026-10-24 | Preservar os originais fora do novo repositório | Não perder notas, configurações ou histórico |
| 2026-10-24 | Não versionar dados nem outputs locais | Respeitar termos e evitar divulgação de materiais restritos |
| 2026-10-24 | CLI inicial reproduz `smooth50` | Ponto de partida explícito, sem alegar melhoria |
| 2026-10-24 | Documentação reorganizada em secções `[00]`–`[99]`, cada uma com índice | Navegação previsível; o conhecimento tem de sobreviver à sessão |
| 2026-10-24 | Proibições oficiais transcritas para `AGENTS.md` | Um agente que não conhece a linha pode atravessá-la |
| 2026-10-24 | Validação primária em **outros jogos** (DFL), não nos 5 min públicos | 17 posses não ordenam variantes; afinar ali é proibido e engana |
| 2026-10-24 | Métrica de decisão é `spellF1` em `leave-one-match-out` | Punir sobre-segmentação é o objetivo da competição |
| 2026-10-24 | Não ajustar pesos/offsets na janela pública (nem "só quatro") | Duas equipas fizeram-no; é risco de desqualificação |
| 2026-10-24 | Reimplementar ideias da concorrência, não copiar código | Atribuição limpa e compreensão real; copiar dá no máximo um empate |
| 2026-10-24 | Prioridade a bordas de interrupção e durações, não a deteção de bola | Teto medido da bola perfeita: +0,03; bordas erram segundos |
| 2026-10-25 | Montar os 9 assets em `data/` (vídeos copiados com reflink) e correr E0 | Validar a pipeline com dados reais sem duplicar espaço físico |
| 2026-10-25 | Baseline real é o fallback; só substituir com ganho medido em DFL | O objetivo é bater 0,2433, não publicar uma variante pior |
| 2026-10-25 | A referência DFL ~0,61 não é o piso do jogo-alvo | Protocolos e convenções diferentes; o alvo verificado é 0,2433 |

O URL remoto foi decidido em 2026-10-24. A licença do código da equipa continua por decidir (`?`).
