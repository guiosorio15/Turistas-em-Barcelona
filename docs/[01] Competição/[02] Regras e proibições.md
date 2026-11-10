# Regras e proibições

**Estado:** vivo · **Fonte:** `vendor/mtah/RULES.md` (oficial) e `docs/[06] Registo/[01] Decisões.md`

## O princípio

Duas condições para **qualquer** método:

1. Os organizadores conseguem **aceder e correr** aquilo de que dependemos.
2. O documento técnico **explica** o que fizemos e porquê.

Dentro disso, "any method at all".

## Proibido (lista dura)

| # | Proibição | O que inclui na prática |
|---|---|---|
| 1 | **Anotar à mão** | Escrever labels a ver o vídeo; corrigir à mão a saída do algoritmo (frame a frame, por segmentos ou só nas transições); usar GT que tenha vazado |
| 2 | **Labels humanas deste jogo** | Nem para submeter, nem para treinar, nem para validar. A linha é **o jogo**, não a quantidade |
| 3 | **GT privado ou dados humanos deste jogo** | Event data (Opta, StatsBomb, Wyscout, LaLiga), tracking corrigido, dados de posse, anotações — de qualquer fonte |
| 4 | **Afinar nos 5 minutos públicos** | Não é treino nem conjunto de afinação; serve para verificar alinhamento, contrato e semântica |
| 5 | **CSV não regenerável** | Correr o repo sobre os dados tem de produzir *o mesmo ficheiro*, não "parecido" |
| 6 | **Redistribuir dados** | Inclui commits e derivados que reconstruam o jogo (export frame a frame, vídeo cortado) |
| 7 | **Alterar o scorer oficial** | O scorer é a lei; não se toca |
| 8 | **Depender do inacessível** | Modelo interno privado, dataset que não se pode partilhar |

## Permitido (e é aqui que se ganha)

- Qualquer linguagem, framework, modelo pré-treinado (comercial ou aberto), LLM local ou alojado.
- **Deteção, tracking, homografia e reconhecimento de eventos próprios** — melhorar ou substituir os dados fornecidos é explicitamente bem-vindo.
- **Dados de outros jogos**, anotados à mão ou não, em qualquer quantidade.
- Aprendizagem não supervisionada, auto-supervisionada e **pseudo-etiquetas geradas por algoritmo**.
- Métodos clássicos sem treino.
- **Ver o vídeo e inspecionar os dados** para compreender, depurar e desenhar features.

## A linha cinzenta que mais importa

> Ver o vídeo **é permitido**. Transformar o que se viu em labels, correções, ou em regras e constantes ligadas a frames específicos deste jogo **não é**.

Consequências práticas para nós:

- Podemos olhar para os 5 minutos públicos e dizer "aqui um toque não muda a posse". Não podemos escolher o custo de transição que maximiza `spellF1` nesses 17 posses.
- Podemos inspecionar o broadcast e concluir "close-ups indicam bola morta". Não podemos ajustar os pesos do classificador nesses frames.
- A nossa validação séria é em **outros jogos** (DFL/Sportec, Metrica sample-data).

## Dados

- Licença só para a competição; os termos do enrollment são a autoridade.
- O repositório de entrega é público: `data/` fica fora do Git (já está no `.gitignore`).
- Não publicar derivados que permitam reconstruir o pacote.

## Se estivermos perto da linha

Perguntar **antes** de construir. Uma resposta antes do prazo vale mais do que uma desqualificação depois. Ver [05] Perguntas abertas.

## Atualização oficial de 2026-11-07

Mensagem dos organizadores recebida pela equipa; **tem precedência** sobre documentação, e-mails anteriores e respostas individuais.

**Não permitido**
- Verificar a saída contra o vídeo.
- Etiquetas manuais, dados humanos ou qualquer dado criado à mão sobre o jogo fornecido.
- Enviar os dados fornecidos para serviços de IA.
- Treinar, ajustar ou calibrar o algoritmo no ground truth de posse ou no vídeo fornecido.

**Permitido**
- Verificações automáticas usando apenas os dados fornecidos.
- Inspecionar os dados e o vídeo para compreender o que conta como posse.
- Usar como input o vídeo, o tracking automático, o Smart Tagging ou outros dados gerados, desde que o algoritmo não tenha sido treinado no GT nem no vídeo.
- Fornecer ficheiros de passos intermédios.
- Usar qualquer dataset cuja licença o permita.

**Consequência para nós:** treino, hiperparâmetros e custos de transição só em DFL/outros jogos. O público serve para contrato, alinhamento e semântica — nunca para escolher variantes. Não comparar a saída com o vídeo.
