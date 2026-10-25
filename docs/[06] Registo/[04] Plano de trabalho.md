# Plano de trabalho

Marcos propostos; não são prazos comunicados pelos organizadores.

1. **Base reproduzível:** obter o dataset completo, correr baseline e validar CSV; confirmar os cinco nomes e criar o remoto da equipa.
2. **Dados fiáveis:** verificar alinhamento por parte, coordenadas métricas, ausência de bola e consistência das fontes.
3. **Primeiro modelo:** máquina de estados com confiança de controlo e deteção separada de interrupções.
4. **Melhorias:** integração de Smart Tagging, modelo temporal e confirmação por passes. Seleção metodológica com outros jogos ou dados sintéticos, sem afinação no teste fornecido.
5. **Entrega:** congelar dependências e configuração, regenerar CSV, comparar hashes, validar o ficheiro exato, terminar relatório e submeter até 2026-11-17.

## Checklist
- [ ] Obter tracking, vídeos e homografias em falta.
- [ ] Confirmar nomes e frentes dos cinco elementos.
- [ ] Criar e configurar URL Git da equipa.
- [ ] Reproduzir baseline com dados reais.
- [ ] Implementar e verificar modelo próprio.
- [ ] Testar num segundo computador a partir de um clone.
- [ ] Validar CSV, documento e reprodução final.

**Próximo passo:** obter as restantes partes do dataset e executar `uv run --locked turistas check-data --baseline-only`.
A fila técnica detalhada vive em `../[04] Método/[05] Plano de experimentos.md` (E0–E11).

## Revisão de 2026-10-24 (após investigação)

O plano original assumia construir o modelo do zero, só com heurísticas. A investigação mudou duas coisas:

1. **O piso real é ~0,61 `spellF1`** (medido por uma equipa em 7 jogos DFL), não 0,2433. O marco 3 ("primeiro modelo") tem de ser avaliado contra esse valor, não contra a baseline.
2. **A validação tem de ser em outros jogos.** Sem isso, qualquer decisão é opinião. Passa a ser o marco 1b, antes do modelo.

Ordem revista: dados → **protocolo DFL** → baseline aprendida → descodificador com durações → bordas → sequência/ensemble → entrega.
