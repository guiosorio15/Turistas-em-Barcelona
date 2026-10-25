# Ideias — hipóteses a experimentar

**Estado:** vivo · atualizado 2026-10-24

Nada aqui é resultado medido. Cada ideia tem hipótese, teste e estado. A ordem é de **execução**, não de entusiasmo.

## Tabela de hipóteses

| ID | Hipótese | Porque pode funcionar | Como testar | Estado |
|---|---|---|---|---|
| **H1** | Treinar em **outros jogos** com tracking degradado bate qualquer regra manual | Há labels por frame noutros jogos; a degradação aproxima os domínios | Leave-one-match-out em 7 jogos DFL | **a fazer** |
| **H2** | **Descodificação com durações** (HSMM) bate Viterbi de custo fixo | A distribuição de durações de posse é estável; o custo fixo não a representa | Comparar `spellF1` em DFL com os mesmos log-odds | a fazer |
| **H3** | Features de **forma da equipa** salvam os 41 % sem bola | Só com forma, 83 % dos frames vivos são identificados corretamente | Ablação: só forma vs só bola vs ambas | a fazer |
| **H4** | **Bordas de interrupção** detetadas frame a frame valem mais que qualquer melhoria de classificador | Todos os sistemas erram aí; o líder usa deslocamento constante | Medir erro de borda (frames) no GT público como diagnóstico, em DFL como métrica | a fazer |
| **H5** | **Modelo de sequência** (TCN/Transformer) sobre as features bate o GBM | Erros de frame são correlacionados no tempo; o GBM não vê sequência | Mesmas features, mesma decodificação, comparar DFL | a fazer |
| **H6** | **Ensemble** DFL-supervisionado + auto-supervisionado ganha aos dois | Erros descorrelacionados (fontes de treino diferentes) | Média de log-odds, avaliada em DFL | a fazer |
| **H7** | **Self-training** no jogo-alvo adapta a convenção (4,2 vs 8 turnovers/min) | Offline e sem labels humanos; permitido explicitamente | 1 ronda de pseudo-labels, medir em DFL e sanidade no jogo | a fazer |
| **H8** | **Áudio/silvo** (se existir) dá bordas quase perfeitas | O árbitro apita exatamente na paragem | Inspecionar faixa áudio do mp4 tático | por verificar |
| **H9** | **Bola fora** = trajetória sai do polígono do campo → `D` imediato | Física simples, sem treino, e ataca a borda | Regra + validação no GT público (só diagnóstico) | a fazer |
| **H10** | Excluir o **árbitro** dos toques melhora a posse | O árbitro toca na bola e não tem equipa | Detetar por cor/posição; medir em DFL | risco médio |
| **H11** | **Deteção própria de bola** nas oclusões | Teto medido: +0,03 | Protótipo YOLO em 200 frames; medir | **baixa prioridade** |
| **H12** | Alinhar o **broadcast** para detetar close-ups como sinal de bola morta | 76 % dos frames mortos sem campo vs 3 % dos vivos | Alinhamento automático + pesos justificados fora da janela pública | a fazer, com cuidado regulamentar |

## Ideias originais da equipa (preservadas)

### 1. Posse com memória e histerese
Combinar distância métrica à bola, tempo de proximidade, velocidade relativa e apoio da equipa. Manter a equipa até surgir evidência consistente de controlo adversário.
*Vantagem esperada:* reduzir fragmentação. *Risco:* atrasar transições ou eliminar posses curtas legítimas.

### 2. Interrupções como decisão separada
Usar Smart Tagging de recomeços, movimento, posição e contexto coletivo. Bola imóvel não basta para decidir `D`; ausência de bola não significa interrupção.

### 3. Smart Tagging como evidência
Converter intervalos em features temporais e confiança, sem os tratar como verdade. Tratar eventos sobrepostos, lacunas e contradições explicitamente.

### 4. Modelo de sequência
Começar por máquina de estados explicável. Comparar com HMM ou HSMM, com estados `H/A/D` e durações plausíveis. A competição é offline: evidência futura pode ajudar a resolver oclusões, sem consultar etiquetas humanas.
Parâmetros devem ser justificados por regras gerais, outros jogos ou simulação; nunca afinados nos cinco minutos públicos.

### 5. Modelo de passe da equipa
As notas originais propõem detetar saída da bola de uma área de controlo e receção, incluindo confirmação por passes consecutivos.
Usar como reforço: exigir sempre dois passes atrasaria recuperações legítimas.
Calcular velocidade por derivação temporal da posição e aceleração por derivação da velocidade; suavizar ruído e rejeitar saltos do tracking.
Uma mudança de trajetória pode sugerir toque, mas não prova controlo. Bola a passar perto de um colega não implica receção.

### 6. Visão apenas onde compensar
Aproveitar primeiro o tracking já fornecido. Um detetor local complementar pode ajudar nas oclusões, com maior custo de desenvolvimento e computação.

## Ordem sugerida (revista em 2026-10-24)

Dados e protocolo → H1 (baseline aprendida) → H2 (descodificador) → H3/H9 (bola ausente e bola fora) → H4/H8 (bordas) → H5/H6 (sequência e ensemble) → H7 (adaptação) → H11 (visão, só se sobrar tempo).

## Referências internas
- [Modelo de Passe original](../[99]%20Arquivo/Notas%20originais/Modelo%20de%20Passe.md)
- [TeamPos Model original](../[99]%20Arquivo/Notas%20originais/TeamPos%20Model.md)
- [Estado da arte]([01]%20Estado%20da%20arte.md) · [Resultados negativos]([04]%20Resultados%20negativos.md)
