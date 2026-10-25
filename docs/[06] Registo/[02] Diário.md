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
