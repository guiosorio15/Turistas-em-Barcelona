# Verificação — 2026-10-24/25

- Python 3.11 obtido por uv; ambiente base e lock instalados com sucesso.
- Seis testes passaram: dados em falta, precedência do caminho explícito, contrato CSV, configuração segura, encaminhamento para scorer público e reprodução sintética.
- A reprodução sintética executou a baseline oficial duas vezes, gerou CSVs de 199 319 frames aceites pelo validador e confirmou igualdade dos hashes. Não constitui resultado no jogo real.
- Avaliação das quatro baselines incluídas executada com sucesso, sem alterar o scorer.
- Clone local em pasta com espaços, com `.venv` nova: instalação, seis testes e avaliação passaram.
- Extra de notebooks instalado; imports de kloppy/metrica, matplotlib e notebook verificados, bem como comando de versão Jupyter.
- Todos os ficheiros exportados do upstream coincidem byte a byte com o commit registado em `vendor/mtah/UPSTREAM.md`.
- Ligações Markdown locais da documentação da equipa verificadas.
- Git apenas acompanha os README de `data/` e `outputs/`; assets e resultados locais excluídos.
- **E0 em 2026-10-25:** os 9 assets foram montados localmente; `check-data` passou 9/9. `turistas reproduce` gerou 199 319 linhas, **669 posses** e 35,9% `D`; o CSV é byte-a-byte igual ao `baseline_smooth50` oficial (`sha256 6d4e04b8...`).
- `turistas evaluate --results outputs/submissions --bootstrap 1000`: `spellF1` público **0,3256** (IC bootstrap 0,214–0,447) e `macroF1` **0,6207**. A amostra de 17 posses não ordena variantes.

## Limites

A baseline real foi executada em 2026-10-25; a limitação de dados está resolvida neste checkout. O modelo E2 existe, a submissão é válida e o LOMO está concluído; E5/E2b negativos e E2 congelado.

## 2026-11-07 — E1/E2 e modelo próprio

- **9 testes passam** com `PYTHONPATH=src`: 6 de integração, parser ATD e Viterbi.
- O editable install do uv falha neste path por `[01]`/`Cérebro` (o `.pth` é lido em cp1252). Num clone sem esses caracteres, `uv run --locked` funciona. Workaround local: `PYTHONPATH=src`.
- `turistas evaluate` falha neste path porque o scorer oficial usa `glob` sobre `[01]`; correr com `--gt` explícito e `--results` relativo.
- Baseline: 199 319 linhas, 669 posses, 35,9% `D`, `spellF1` 0,3256; labels iguais ao oficial; o hash difere por CRLF vs LF.
- Modelo E2: 7 jogos DFL; 1 002 644 frames; DFL degradado **0,443**; LOMO **0,525 ± 0,037**; full-match **43,1% `D`/415 posses**; público **0,5455** (sanidade, não seleção).
- E5/E2b testados e negativos: bola fora 0,403–0,421 e três classificadores 0,411 vs 0,443; N13/N14. E2 congelado.
Não foi testada a interface gráfica Jupyter, Windows ou macOS. A CI está preparada para os três sistemas; confirmar no GitHub se já correu no remoto.
Remoto configurado: `git@github.com:guiosorio15/Turistas-em-Barcelona.git`, privado. O commit inicial criado no GitHub foi integrado por merge, preservando ambos os históricos. A validação inicial por clone local mantém-se aplicável; a CI remota terá o seu próprio estado no GitHub.

## Particularidade deste computador

O comando Git local usa um wrapper que falhou ao localizar `upload-pack` no primeiro clone local. O teste foi executado com `git clone --upload-pack=/usr/bin/git-upload-pack <origem-local> <destino>` e passou. Não foi alterada a configuração global de Git. Esta particularidade é do ambiente local, não uma opção exigida para clones GitHub.

O executável uv foi instalado em `~/.local/bin/uv`, disponível no PATH deste computador.
