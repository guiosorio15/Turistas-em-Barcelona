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
