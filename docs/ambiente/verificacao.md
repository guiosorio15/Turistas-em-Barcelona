# Verificação inicial — 2026-10-24

- Python 3.11 obtido por uv; ambiente base e lock instalados com sucesso.
- Seis testes passaram: dados em falta, precedência do caminho explícito, contrato CSV, configuração segura, encaminhamento para scorer público e reprodução sintética.
- A reprodução sintética executou a baseline oficial duas vezes, gerou CSVs de 199 319 frames aceites pelo validador e confirmou igualdade dos hashes. Não constitui resultado no jogo real.
- Avaliação das quatro baselines incluídas executada com sucesso, sem alterar o scorer.
- Clone local em pasta com espaços, com `.venv` nova: instalação, seis testes e avaliação passaram.
- Extra de notebooks instalado; imports de kloppy/metrica, matplotlib e notebook verificados, bem como comando de versão Jupyter.
- Todos os ficheiros exportados do upstream coincidem byte a byte com o commit registado em `vendor/mtah/UPSTREAM.md`.
- Ligações Markdown locais da documentação da equipa verificadas.
- Git apenas acompanha os README de `data/` e `outputs/`; assets e resultados locais excluídos.

## Limites

Não foi possível executar a baseline no jogo real: faltam os dois ficheiros de tracking tático. Apenas o Smart Tagging está disponível.
Não foi testada a interface gráfica Jupyter, Windows ou macOS. A CI está preparada para os três sistemas, mas ainda não correu num remoto.
Não há URL remoto da equipa nem publicação. O histórico local inclui a estrutura preparada.

## Particularidade deste computador

O comando Git local usa um wrapper que falhou ao localizar `upload-pack` no primeiro clone local. O teste foi executado com `git clone --upload-pack=/usr/bin/git-upload-pack <origem-local> <destino>` e passou. Não foi alterada a configuração global de Git. Esta particularidade é do ambiente local, não uma opção exigida para clones GitHub.

O executável uv foi instalado em `~/.local/bin/uv`, disponível no PATH deste computador.
