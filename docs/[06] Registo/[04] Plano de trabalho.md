# Plano de trabalho

Marcos propostos; não são prazos comunicados pelos organizadores.

1. **Base reproduzível:** obter o dataset completo, correr baseline e validar CSV; confirmar os cinco nomes e criar o remoto da equipa.
2. **Dados fiáveis:** verificar alinhamento por parte, coordenadas métricas, ausência de bola e consistência das fontes.
3. **Primeiro modelo:** máquina de estados com confiança de controlo e deteção separada de interrupções.
4. **Melhorias:** integração de Smart Tagging, modelo temporal e confirmação por passes. Seleção metodológica com outros jogos ou dados sintéticos, sem afinação no teste fornecido.
5. **Entrega:** congelar dependências e configuração, regenerar CSV, comparar hashes, validar o ficheiro exato, terminar relatório e submeter até 2026-11-17.

## Checklist
- [x] Obter tracking, vídeos e homografias em falta.
- [ ] Confirmar nomes e frentes dos cinco elementos.
- [x] Criar e configurar URL Git da equipa.
- [x] Reproduzir baseline com dados reais.
- [ ] Implementar e verificar modelo próprio.
- [ ] Testar num segundo computador a partir de um clone.
- [ ] Validar CSV, documento e reprodução final.

**Próximo passo:** implementar o primeiro modelo próprio (E1–E2) e manter a baseline `smooth50` como fallback. O caminho crítico deixou de ser os dados.
A fila técnica detalhada vive em `../[04] Método/[05] Plano de experimentos.md` (E0–E11).

## Revisão de 2026-10-24 (após investigação)

O plano original assumia construir o modelo do zero, só com heurísticas. A investigação mudou duas coisas:

1. **A referência DFL é ~0,61 `spellF1`** (medido por uma equipa em 7 jogos DFL), mas **não é o piso do jogo-alvo**. O único número verificado no alvo é 0,2433 (baseline full) e 0,3256 (público). 0,61 serve para o protocolo DFL, não para o ranking.
2. **A validação tem de ser em outros jogos.** Sem isso, qualquer decisão é opinião. Passa a ser o marco 1b, antes do modelo.

Ordem revista: dados → **protocolo DFL** → baseline aprendida → descodificador com durações → bordas → sequência/ensemble → entrega.

## Revisão de 2026-10-25 (E0 concluído)

- 9/9 assets montados; baseline real validada: 0,3256 público, 0,6207 macro, **669 posses**, 35,9% `D`; CSV byte-a-byte igual ao oficial (`sha256 6d4e04b8...`).
- O caminho crítico mudou: já não é obter dados; é construir e validar o modelo. E1 (DFL) tem **timebox de 2 dias**.
- A baseline `smooth50` fica como fallback válido. Nenhuma variante própria entra sem ganho medido em DFL.
