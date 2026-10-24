# Arquitetura

## Implementado
A CLI `turistas` resolve a raiz do checkout, verifica assets, chama os scripts oficiais em subprocessos e encaminha resultados para `outputs/`.
`reproduce` lê TOML, gera a variante oficial configurada numa pasta temporária, valida-a e guarda um manifesto com parâmetros, dependências, hash dos inputs mínimos, código e CSV.
O comando é determinístico para a baseline oficial com os mesmos inputs, configuração e versões. A equivalência com dados reais ainda depende do pacote em falta.
`vendor/mtah/` fica inalterado durante a execução.

## A implementar
Leitura/alinhamento → features geométricas e táticas → confiança de controlo e bola em jogo → resolução temporal → etiquetas → CSV → validação oficial.
Separar módulos por responsabilidade quando forem implementados; evitar lógica de produção apenas em notebooks.

## Limites
Esta distribuição destina-se a um checkout do repositório; a CLI depende de `vendor/` e `configs/` na raiz. Um wheel isolado não é uma distribuição autónoma.
O manifesto é local e contém hashes de inputs restritos; não o publicar automaticamente.
