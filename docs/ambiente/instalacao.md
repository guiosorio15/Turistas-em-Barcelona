# Instalação noutro computador

Pré-requisitos: Git, acesso à Internet na primeira instalação e uv. Seguir a [instalação oficial do uv](https://docs.astral.sh/uv/getting-started/installation/).
O projeto fixa Python 3.11 em `.python-version`; uv obtém essa versão e cria `.venv`.

## Clonar
O repositório é privado; a conta precisa de acesso e de uma chave SSH configurada no GitHub.

```bash
git clone git@github.com:guiosorio15/Turistas-em-Barcelona.git
cd Turistas-em-Barcelona
```

Em alternativa, clonar por HTTPS: `https://github.com/guiosorio15/Turistas-em-Barcelona.git`, usando autenticação GitHub.
O repositório da equipa contém a integração completa; o upstream dos organizadores contém apenas a referência oficial.

## Linux, macOS e Windows PowerShell
Os comandos seguintes são iguais nos três sistemas, executados na raiz:

```bash
uv sync --locked
uv run --locked turistas --help
uv run --locked turistas evaluate
uv run --locked python -m unittest discover -s tests -v
```

Não é necessário ativar o ambiente virtual. Para notebooks: `uv sync --locked --extra notebooks` e `uv run --locked --extra notebooks jupyter notebook`.
O extra de notebooks está fixado no lock e foi instalado em Linux; imports de kloppy/metrica, matplotlib e notebook verificados. A interface gráfica e os restantes sistemas operativos ainda não foram testados.

## Dados
Copiar os dados autorizados separadamente, nunca através de Git. Preferir `--data-dir "/caminho com espaços/dataset"`.
Em Linux/macOS também é possível `export MTAH_DATA_DIR="/caminho/dataset"`.
Em PowerShell: `$env:MTAH_DATA_DIR = "C:\dados\dataset"`.
`.env.example` é um exemplo: copiar para `.env` não define variáveis automaticamente.

## Problemas frequentes
- Falta de tracking: descarregar as restantes partes do pacote; o ZIP inicial contém apenas Smart Tagging.
- Erro de importação: executar `uv sync --locked` e usar `uv run --locked`.
- Lock desatualizado: não remover `--locked`; rever intencionalmente a alteração de dependências.
- Não há GPU obrigatória para a baseline.
