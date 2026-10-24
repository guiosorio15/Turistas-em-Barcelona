# Regras dos agentes — Turistas de la Nave

Este ficheiro é a fonte central de direções para Codex, Claude Code e OpenCode.
Lê-o antes de alterar o repositório. Escreve documentação em PT-PT.

## Contexto e arquitetura
- Equipa: Turistas de la Nave, cinco elementos; nomes e responsáveis por confirmar.
- Objetivo: produzir um CSV algorítmico de posse de bola para a fase 1 do More Than a Hack 2027.
- `src/turistas/`: código da equipa; `configs/`: parâmetros; `tests/`: verificações.
- `vendor/mtah/`: referência oficial com versão em `UPSTREAM.md`. Preservar licença e autoria.
- `docs/projeto/`: âmbito, tarefas, ideias e decisões.
- `docs/tecnica/`: dados, arquitetura, avaliação e relatório.
- `docs/ambiente/`: instalação, dados locais e comandos.
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

## Estado inicial
A CLI reproduz a baseline oficial; ainda não implementa um modelo melhorado.
O dataset disponível na preparação inicial só contém o XML de Smart Tagging.
Consultar `docs/projeto/plano.md` para o próximo trabalho.
