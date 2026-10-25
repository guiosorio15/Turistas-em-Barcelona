# Arquitetura

## Implementado
A CLI `turistas` resolve a raiz do checkout, verifica assets, chama os scripts oficiais em subprocessos e encaminha resultados para `outputs/`.
`reproduce` lê TOML, gera a variante oficial configurada numa pasta temporária, valida-a e guarda um manifesto com parâmetros, dependências, hash dos inputs mínimos, código e CSV.
O comando é determinístico para a baseline oficial com os mesmos inputs, configuração e versões. A equivalência com dados reais ainda depende do pacote em falta.
`vendor/mtah/` fica inalterado durante a execução.

## A implementar
Leitura/alinhamento → features geométricas e táticas → confiança de controlo e bola em jogo → resolução temporal → etiquetas → CSV → validação oficial.
Separar módulos por responsabilidade quando forem implementados; evitar lógica de produção apenas em notebooks.

## Alvo (2026-10-24)

```
src/turistas/
├─ atd.py          leitura do ATD (frames, slots, bola, equipas)
├─ degrade.py      degradação do tracking de outros jogos (treino)
├─ features.py     features por frame, sem identidades  → docs/[04] Método/[02] Features
├─ models.py       classificadores: morto/vivo, H/A, quem recomeça
├─ decode.py       Viterbi/HSMM com durações e custos    → docs/[04] Método/[03] Decodificação
├─ edges.py        refinamento de bordas (bola fora, paragens)
├─ evaluate.py     protocolo em outros jogos            → docs/[04] Método/[04] Avaliação
└─ cli.py          check-data · reproduce · validate · evaluate · train · cv
```

Regra: **a mesma função de features serve o jogo-alvo e os jogos de treino**. Se divergirem, a validação deixa de valer.

## Limites
Esta distribuição destina-se a um checkout do repositório; a CLI depende de `vendor/` e `configs/` na raiz. Um wheel isolado não é uma distribuição autónoma.
O manifesto é local e contém hashes de inputs restritos; não o publicar automaticamente.
