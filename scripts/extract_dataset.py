"""Extrai os assets do pacote fornecido a partir dos ZIPs em ~/Downloads.

Os downloads do browser podem ficar com nomes temporários (`*.tmp`). O script
inspeciona o conteúdo, ignora ficheiros que não sejam ZIP e extrai apenas
`tactical/` e `broadcast/` para data/. Os dados não entram no Git.

Uso:
    uv run --locked python scripts/extract_dataset.py
"""
from pathlib import Path
import os
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOWNLOADS = Path(os.path.expanduser("~")) / "Downloads"
PREFIX = "More Than A Hack 2027 - Initial Challenge - Dataset/"


def candidates():
    for pattern in ("*.tmp", "*.zip", "*.part"):
        yield from DOWNLOADS.glob(pattern)


def extract(path):
    if not zipfile.is_zipfile(path):
        return []
    written = []
    with zipfile.ZipFile(path) as archive:
        for entry in archive.infolist():
            if not entry.filename.startswith(PREFIX):
                continue
            relative = entry.filename[len(PREFIX):]
            if not (relative.startswith("tactical/") or relative.startswith("broadcast/")):
                continue
            destination = DATA / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.is_file() and destination.stat().st_size == entry.file_size:
                written.append((relative, "já existe"))
                continue
            temporary = destination.with_suffix(destination.suffix + ".part")
            with archive.open(entry) as source, temporary.open("wb") as target:
                shutil.copyfileobj(source, target, 1 << 20)
            if temporary.stat().st_size != entry.file_size:
                temporary.unlink()
                raise IOError("tamanho errado em {}".format(entry.filename))
            temporary.replace(destination)
            written.append((relative, "{:.1f} MB".format(entry.file_size / 1e6)))
    return written


def main():
    seen = set()
    for path in sorted(candidates()):
        try:
            written = extract(path)
        except (OSError, zipfile.BadZipFile) as error:
            print("ignorado {}: {}".format(path.name, error), file=sys.stderr)
            continue
        for relative, detail in written:
            if relative not in seen:
                print("OK {} ({})".format(relative, detail))
                seen.add(relative)
    missing = 9 - len(seen)
    print("{} assets extraídos; {} dos 9 ainda em falta.".format(len(seen), missing))
    return 0 if seen else 1


if __name__ == "__main__":
    raise SystemExit(main())
