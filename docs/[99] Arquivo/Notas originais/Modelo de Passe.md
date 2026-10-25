Detetar 2 pontos:
- Tentativa de passe
- Receção do passe

![Esquema](Images/Pasted%20image%2020261021202639.png)

A deteção da tentativa de passe pode ser feita a partir da bola deixar a área de um jogador

A receção pode ser caso o Modelo de Posse (nota referida, não encontrada nos originais) ative para um jogador da mesma equipa OU caso seja detetado uma outra tentativa de passe da mesma equipa

Edge case:
![Esquema](Images/Pasted%20image%2020261021203415.png)

Passe de 1 para 3, passa a área do 2 mas o 2 não toca. 
Opções:
- Modelo que visualmente detete toque e definir passe a partir daí (pixeis de "pé" perto de pixeis de "bola")
- Ver mudanças bruscas de trajetória - com historico de frames calcular integrada para velocidade e/ou aceleração e ao detetar falta de linearidade considerar toque
NOTA: QUALQUER UMA DESTAS OPCOES PODE SER O TRIGGER PARA A DETEÇÃO DA TENTATIVA DE PASSE INICIAL
