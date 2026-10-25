# Regras dos agentes — Turistas de la Nave

Este ficheiro é a fonte central de direções para Codex, Claude Code e OpenCode.
Lê-o antes de alterar o repositório. Escreve documentação em PT-PT.

## Contexto e arquitetura
- Equipa: Turistas de la Nave, cinco elementos; nomes e responsáveis por confirmar.
- Objetivo: produzir um CSV algorítmico de posse de bola para a fase 1 do More Than a Hack 2027.
- `src/turistas/`: código da equipa; `configs/`: parâmetros; `tests/`: verificações.
- `vendor/mtah/`: referência oficial com versão em `UPSTREAM.md`. Preservar licença e autoria.
- `docs/[00] Índice.md`: portal da documentação; toda a navegação começa aqui.
- `docs/[01] Competição/`: regras, métricas, calendário, perguntas abertas.
- `docs/[02] Dados/`: inventário, ATD, Smart Tagging, homografia e broadcast.
- `docs/[03] Investigação/`: estado da arte, repositórios, concorrência, negativos, ideias.
- `docs/[04] Método/`: arquitetura, features, decodificação, avaliação, experimentos.
- `docs/[05] Operação/`: instalação, comandos, verificação.
- `docs/[06] Registo/`: decisões, diário, equipa, plano.
- `docs/[99] Arquivo/`: notas originais preservadas.
- `data/` e `outputs/`: materiais locais excluídos do Git, exceto os README.

## Regras
1. Preservar notas, ficheiros originais e histórico. Nunca apagar sem autorização.
2. Nunca inventar resultados, responsáveis, fontes ou dados em falta: usar `?`.
3. Não incluir datasets restritos, vídeos, tracking, excertos ou exportações que os reconstruam no Git.
4. Não enviar materiais restritos para LLMs alojados ou outros serviços externos.
5. Ler as regras oficiais atuais antes de mudar a metodologia. Não usar anotações humanas deste jogo, dados humanos de terceiros sobre este jogo, correções manuais ou regras ligadas a frames específicos.
6. Os cinco minutos públicos servem para verificar a pipeline; nunca para treino, seleção de modelos ou afinação de parâmetros. Dados anotados de outros jogos podem ser usados conforme as regras oficiais.
7. Preservar a avaliação oficial; não alterar o scorer para melhorar resultados.
8. Usar `uv sync --locked`; atualizar `uv.lock` intencionalmente quando mudarem dependências.
9. Reproduzir via CLI da equipa; manter parâmetros, versão do código e hashes dos resultados.
10. Antes de concluir, executar `uv run --locked python -m unittest discover -s tests -v` e `uv run --locked turistas evaluate`. Se faltarem dados, declarar a limitação.
11. Não fazer push, publicar ou submeter sem instrução do utilizador.
12. Não criar agentes auxiliares sem pedido explícito.

## Proibido — regras oficiais (`vendor/mtah/RULES.md`)

Estas linhas são duras: violá-las invalida a submissão, independentemente do score.
Se uma abordagem estiver perto da linha, **perguntar antes de construir** (issue aos organizadores).

1. **Anotar dados à mão.** As etiquetas têm de sair de um algoritmo. Inclui escrever labels a olhar para o vídeo, corrigir à mão a saída do algoritmo (frame a frame, por segmentos ou só nas transições) e usar um ground truth que tenha vazado.
2. **Etiquetas humanas do jogo fornecido, em qualquer quantidade e para qualquer fim** — nem para submeter, nem para treinar, nem para validar. A linha é **o jogo**, não a quantidade. Etiquetas manuais de **outros jogos** são permitidas em qualquer quantidade.
3. **Ground truth privado ou qualquer dado humano sobre este jogo**, de qualquer fonte: event data (Opta, StatsBomb, Wyscout, LaLiga), tracking corrigido, dados de posse, anotações. Sobre outros jogos é permitido.
4. **Afinação nos cinco minutos públicos.** Servem para verificar a pipeline (alinhamento, contrato, semântica das labels); nunca para treinar, escolher variantes ou ajustar parâmetros. Ver `docs/[01] Competição/[03] Métricas.md`.
5. **Submeter um CSV que o repositório não regenere** exatamente a partir dos dados fornecidos.
6. **Redistribuir os dados do jogo** ou publicar derivados que os reconstruam (export de tracking frame a frame, vídeo cortado). O repositório da entrega é público: os dados não podem lá estar.
7. **Alterar o scorer oficial** para melhorar resultados.
8. **Depender de algo que os organizadores não possam inspecionar e correr** — modelo interno privado, dataset inacessível.

Observar o vídeo e inspecionar os dados para compreender, depurar e desenhar features **é permitido**. O que não é permitido é transformar o que se viu em labels, correções ou regras/constantes ligadas a frames específicos deste jogo.

## Tudo o resto é permitido — e é aqui que se ganha

O bloco acima é o **único** limite. Dentro dele a resposta oficial é *any method at all*:

- qualquer linguagem, framework e modelo pré-treinado, comercial ou aberto; LLM local ou alojado (nunca enviando dados restritos);
- deteção, tracking, homografia, reconhecimento de eventos ou classificação de posse **próprios** — melhorar ou substituir os dados fornecidos é explicitamente bem-vindo, desde que por algoritmo;
- dados externos de **outros jogos** (públicos ou anotados por nós), aprendizagem não supervisionada ou auto-supervisionada, pseudo-etiquetas geradas por algoritmo, métodos clássicos sem treino.

Nenhuma ideia deve ser descartada por parecer pouco ortodoxa. Uma ideia descarta-se por regra, por evidência medida ou por custo — nunca por hábito. Uma abordagem que ninguém tentou é precisamente o que a competição procura.

## Como decidir (postura crítica)

- Separar sempre **hipótese**, **implementação** e **resultado medido**. Sem número, é opinião.
- O que conta é `spellF1` no jogo completo; os cinco minutos públicos não ordenam variantes (17 posses). Qualquer escolha de parâmetro precisa de justificação por regra geral, por outros jogos ou por simulação.
- Preferir a solução mais simples que sobreviva a um erro de 30 frames e a 41% de frames sem bola. Complexidade só entra quando paga.
- Registar o que falhou, não só o que funcionou: as decisões vivem em `docs/[06] Registo/[01] Decisões.md` e os negativos em `docs/[03] Investigação/[04] Resultados negativos.md`.

## Estado inicial
A CLI reproduz a baseline oficial; ainda não implementa um modelo melhorado.
Em 2026-10-25 os 9 assets foram montados localmente em `data/` (incluindo os dois vídeos) e a baseline real foi validada. O CSV gerado é byte-a-byte igual ao `baseline_smooth50` oficial; `check-data` passou 9/9. O próximo trabalho é o modelo próprio, não mais preparação de dados.
Consultar `docs/[06] Registo/[04] Plano de trabalho.md` para o próximo trabalho, `docs/[04] Método/[05] Plano de experimentos.md` para a fila técnica e `docs/[03] Investigação/[05] Ideias.md` para as hipóteses em aberto. A documentação começa em `docs/[00] Índice.md`.
