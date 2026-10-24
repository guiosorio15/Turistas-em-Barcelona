# Ideias — hipóteses a experimentar

As propostas seguintes não são resultados medidos.

## 1. Posse com memória e histerese
Combinar distância métrica à bola, tempo de proximidade, velocidade relativa e apoio da equipa. Manter a equipa até surgir evidência consistente de controlo adversário.
Vantagem esperada: reduzir fragmentação. Risco: atrasar transições ou eliminar posses curtas legítimas.

## 2. Interrupções como decisão separada
Usar Smart Tagging de recomeços, movimento, posição e contexto coletivo. Bola imóvel não basta para decidir `D`; ausência de bola não significa interrupção.

## 3. Smart Tagging como evidência
Converter intervalos em features temporais e confiança, sem os tratar como verdade. Tratar eventos sobrepostos, lacunas e contradições explicitamente.

## 4. Modelo de sequência
Começar por máquina de estados explicável. Comparar com HMM ou HSMM, com estados `H/A/D` e durações plausíveis. A competição é offline: evidência futura pode ajudar a resolver oclusões, sem consultar etiquetas humanas.
Parâmetros devem ser justificados por regras gerais, outros jogos ou simulação; nunca afinados nos cinco minutos públicos.

## 5. Modelo de passe da equipa
As notas originais propõem detetar saída da bola de uma área de controlo e receção, incluindo confirmação por passes consecutivos.
Usar como reforço: exigir sempre dois passes atrasaria recuperações legítimas.
Calcular velocidade por derivação temporal da posição e aceleração por derivação da velocidade; suavizar ruído e rejeitar saltos do tracking.
Uma mudança de trajetória pode sugerir toque, mas não prova controlo. Bola a passar perto de um colega não implica receção.

## 6. Visão apenas onde compensar
Aproveitar primeiro o tracking já fornecido. Um detetor local complementar pode ajudar nas oclusões, com maior custo de desenvolvimento e computação.

## Ordem sugerida
Dados e baseline → geometria com memória → interrupções → eventos → modelo temporal → visão seletiva.

## Referências internas
- [Modelo de Passe original](../referencias/Modelo%20de%20Passe.md)
- [TeamPos Model original](../referencias/TeamPos%20Model.md)
