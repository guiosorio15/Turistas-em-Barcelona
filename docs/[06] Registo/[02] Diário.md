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
- Pacote de dados em download: ~4,3 GB no momento do registo (por confirmar no fim).

**Descoberto (e importante)**
- Há **20+ equipas** com repositórios públicos. A melhor publica **0,610 `spellF1`** em 7 jogos DFL held-out — muito acima da baseline 0,2433.
- A etiqueta deriva mecanicamente do tracking corrigido: `D` onde a bola está morta, senão a equipa que o tracker nomeia.
- A maioria dos frames sem bola é bola morta; as lacunas curtas já vêm colmatadas pelo fornecedor.
- Duas equipas admitem ter ajustado pesos nos 5 minutos públicos. **Não vamos fazer isso.**

**Próximo**
- E0: validar o pacote (9 assets) e correr a baseline com dados reais.
- E1: loader DFL + degradação + `leave-one-match-out`.

**Riscos abertos**
- Sem dataset completo, nenhum número é real.
- Sem validação em outros jogos, qualquer resultado é opinião.
