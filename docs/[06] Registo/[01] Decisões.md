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
| 2026-11-07 | Clarificação oficial: treino/afinação só em dados externos; público só sanidade | Precedência sobre documentação e respostas anteriores; evita desqualificação |
| 2026-11-07 | Extrair os assets dos `.tmp` do Chrome | ZIPs válidos; o zip pequeno era só uma parte do pacote |
| 2026-11-07 | Jogadores com velocidade convertida km/h→m/s; bola derivada da posição | Unidades diferentes entre DFL e o jogo; `S` crua colapsava o `D` |
| 2026-11-07 | E2 com um GBM de 3 classes + Viterbi de 3 estados | Primeiro número medido em DFL; 4 estados/HSMM só entram se pagarem |
| 2026-11-07 | Modelo dos 7 jogos DFL como candidato; público não seleciona | Mais dados externos; 0,5455 público é sanidade, não resultado |
| 2026-11-07 | E2 validado em `leave-one-match-out`: 0,525 ± 0,037 | Sete jogos DFL; std 0,037; o modelo dos 7 jogos é o candidato |
| 2026-11-08 | Não usar a regra de bola fora nem os três classificadores; congelar E2 | DFL pior em ambos: 0,403–0,421 e 0,411 vs 0,443; N13/N14 |
| 2026-11-08 | E4/HSMM adiado | O prior de durações do DFL não corresponde à convenção mais longa do jogo; sem dados externos adequados seria afinação no alvo |

O URL remoto foi decidido em 2026-10-24. A licença do código da equipa continua por decidir (`?`).
