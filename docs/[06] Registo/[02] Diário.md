# Diário

Registo de sessões. Uma entrada por sessão, com o que se **mediu**, não com o que se sentiu.

---

## 2026-10-24 — Sessão 0: dados, regras e investigação

**Feito**
- Repositório clonado para `[01] Projetos/Hackaton/Turistas-em-Barcelona` (privado; acesso via `gh`).
- `AGENTS.md` recebeu a lista dura de proibições, o perímetro do que é permitido e a postura crítica.
- Documentação reorganizada em secções numeradas `[00]`–`[99]`.
- Investigação inicial: estado da arte, repositórios, concorrência pública e resultados negativos documentados.

**Medido**
- Baseline oficial reproduzida localmente (avaliação pública; ver `outputs/evaluation/`).
- Pacote de dados em download: ~4,3 GB no momento do registo; concluído depois (ver Sessão 1).

**Descoberto (e importante)**
- Há **20+ equipas** com repositórios públicos. A melhor publica **0,610 `spellF1`** em 7 jogos DFL held-out — muito acima da baseline 0,2433.
- A etiqueta deriva mecanicamente do tracking corrigido: `D` onde a bola está morta, senão a equipa que o tracker nomeia.
- Boa parte dos frames sem bola coincide com bola morta; as lacunas curtas já vêm colmatadas pelo fornecedor. (Hipótese a medir: há `D` com bola visível — ver Sessão 1.)
- Duas equipas admitem ter ajustado pesos nos 5 minutos públicos. **Não vamos fazer isso.**

**Próximo**
- E0: validar o pacote (9 assets) e correr a baseline com dados reais.
- E1: loader DFL + degradação + `leave-one-match-out`.

**Riscos abertos**
- Sem dataset completo, nenhum número é real.
- Sem validação em outros jogos, qualquer resultado é opinião.

---

## 2026-10-25 — Sessão 1: E0 concluído com dados reais

**Feito**
- Clone de trabalho neste computador: `~/My Brain/Projetos/turistas-de-la-nave` (a referência `[01] Projetos/Hackaton/...` da Sessão 0 é de outro clone).
- Clone local atualizado para `d7a79b0` (docs reorganizados) e confirmado limpo.
- Os 9 assets foram montados em `data/`: ZIPs `003`–`010` extraídos e os dois MP4 copiados para o contrato (`BAR-ATH_tactical-002.mp4` → `BAR-ATH_tactical.mp4`, `BAR-ATH_broadcast-001.mp4` → `BAR-ATH_broadcast.mp4`).
- `turistas check-data` passou **9/9**.
- `turistas reproduce` gerou a baseline real e o manifesto; `validate` aceitou o CSV.

**Medido**
- 199 319 linhas; **669 posses**; 7,6 s de duração média; 35,9% `D`.
- `spellF1` público **0,3256** (IC bootstrap 0,214–0,447); `macroF1` **0,6207**.
- CSV byte-a-byte igual a `vendor/mtah/evaluation/results/baseline_smooth50.csv` (`sha256 6d4e04b8...`).
- Vídeo tático: 199 319 frames a 25 fps; broadcast: 164 487.
- Seis testes continuam a passar.

**Descoberto (e importante)**
- O “pacote incompleto” era um problema de montagem local, não de acesso: as partes já estavam em `~/Downloads`.
- A baseline real **não** é um bloqueio; o bloqueio passou a ser o modelo próprio.
- O doc dizia 594 posses no jogo completo; o run real diz **669**. Corrigir o número e não o usar sem comando.
- O `spellF1` público tem IC de ~0,23; 0,3256 vs 0,4242 não é uma diferença utilizável para decidir.
- No GT público, em dois dos quatro períodos `D` longos as três baselines escolhem `H`/`A` em 100% dos frames; a `smooth50` só acerta 32,5% dos frames `D` no total. `D` não é apenas “sem bola”: há bola visível e jogador próximo. A proporção de frames sem bola que são `D` continua por medir no tracking completo.

**Próximo**
- E1: loader DFL + degradação + `leave-one-match-out`, com timebox de 2 dias.
- Primeiro modelo: features mínimas + Viterbi de 4 estados; manter a baseline como fallback.
- Confirmar nomes/frentes dos cinco elementos e a hora/fuso do prazo.

---

## 2026-11-07 — Sessão 2: dados, E1/E2 e primeiro modelo

**Feito**
- Clarificação oficial registada em `[01] Competição/[02] Regras e proibições.md`.
- 7 assets não-vídeo extraídos dos `.tmp` do Chrome para `data/`; faltam os dois MP4. O zip pequeno era só `tactical_atd.xml`.
- Baseline real reproduzida: 199 319 linhas, 669 posses, 35,9% `D`, `spellF1` público 0,3256, `macroF1` 0,6207. O hash difere do oficial só por CRLF vs LF.
- 7 jogos DFL/Sportec (CC-BY) descarregados; loader, features coletivas sem identidades, degradação (41% bola, lacunas longas, jogadores em falta, ruído), GBM de 3 classes e Viterbi de 3 estados.
- Modelo treinado em **1 002 644 frames** dos 7 jogos; inferência no jogo com `X` fora das partes e CSV válido.

**Medido**
- DFL, split período 1→2 no J03WMX: `spellF1` **0,576** limpo e **0,443** degradado (244 posses previstas vs 261 reais).
- Jogo completo, modelo dos 7 jogos: **43,1% `D`**, **415 posses**, 8,7 s. Esperado ~45–50% `D`, ~293 posses: a lacuna de domínio mantém-se.
- Sanidade pública isolada: `spellF1` **0,5455**, 27 posses, 10,0 s. São 17 posses e ±0,25 de ruído; **não é critério de seleção**.
- LOMO de 7 jogos: **0,525 ± 0,037** (macro 0,868); 7 folds; 323–376 posses previstas vs 370–511 reais.

**Descoberto (e importante)**
- As velocidades do DFL vêm em km/h e as do ATD do jogo em m/s. Usar `S` diretamente fazia o modelo prever 57% `D`; converter jogadores (÷3,6) e derivar a bola da posição trouxe o full-match para 43%.
- O público e o full-match discordam: o público tem poucas paragens; o full-match tem ~45–50% `D`. Nenhuma variante é escolhida pelo público.
- A convenção DFL (~9 posses/min vivo) continua diferente do jogo (~4); E4/E5 são o próximo trabalho.

**Próximo**
- LOMO fechado: **0,525 ± 0,037**.
- E5: bola fora e set pieces; E4: HSMM/durações. Comparar sempre em DFL.
- Integrar a inferência num comando reproduzível e congelar o CSV final.

---

## 2026-11-08 — Sessão 3: E5/E2b negativos; E2 congelado

**Feito**
- Regra de bola fora testada em DFL com confirmação 3, 25 e 50 frames.
- Três classificadores (morto/vivo + dono) testados contra o GBM único.
- `turistas evaluate` corrigido para passar GT explícito e resultados relativos ao scorer; 9 testes passam e o comando funciona neste path com `PYTHONPATH=src`.

**Medido**
- Bola fora: 0,403 / 0,421 / 0,420 vs 0,443; 18,9k–23,2k frames marcados.
- Três classificadores: 0,411 vs 0,443; macro 0,827 vs 0,835.
- O GBM único mantém LOMO **0,525 ± 0,037**; full-match 43,1% `D`/415 posses; público 0,5455.

**Decisão**
- **Congelar o E2** (GBM de 3 classes + Viterbi). Não usar a regra de bola fora nem os três classificadores.
- E4/HSMM fica adiado: o prior de durações do DFL não corresponde à convenção mais longa do jogo; sem dados externos adequados, seria afinação no alvo.
- O próximo passo é validar a entrega e a reprodução, não abrir mais variantes.

**Próximo**
- Regerar o CSV final, validar e revisar o relatório/reprodução num clone limpo.
- Confirmar a hora/fuso e os nomes da equipa.

---

## 2026-11-08 — Sessão 4: pesquisa e E5b

**Feito**
- Varrimento de 50+ repositórios, papers e indústria; novo doc `[03] Investigação/[06] Métodos 2026-11-08.md`.
- E5b testado em três componentes: Viterbi de 4 estados + restart; p90 como feature; etapa física de bola morta.

**Medido**
- 4 estados: 0,435 vs 0,443; p90 como feature: 0,428 vs 0,443; etapa física: 0,396 vs 0,443 (alive/dead F1 0,914 vs 0,948).
- O E2 mantém **0,525 ± 0,037** e a submissão atual.

**Decisão**
- Os componentes simples do E5b não transferem para o DFL (N15–N17); o E2 fica.
- O caminho com maior potencial restante é **E6: TCN + SkillCorner** (Agamemnon 0,681 externo), que exige download e mapeamento de labels.

**Próximo**
- Decidir E6 vs congelar; revalidar o CSV final e a reprodução.
