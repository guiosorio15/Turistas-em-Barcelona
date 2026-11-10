"""Descarrega o dataset público DFL/Sportec (IDSSE) para data/dfl.

Fonte: https://huggingface.co/datasets/pysport/idsse-data
Licença: CC-BY 4.0. Não versionar os ficheiros; data/ está no .gitignore.

Uso:
    uv run --locked python scripts/fetch_dfl.py
    uv run --locked python scripts/fetch_dfl.py J03WMX J03WN1
"""
from pathlib import Path
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "dfl"
BASE = "https://huggingface.co/datasets/pysport/idsse-data/resolve/main/"

MATCHES = {
    "J03WMX": "DFL-COM-000001",
    "J03WN1": "DFL-COM-000001",
    "J03WOH": "DFL-COM-000002",
    "J03WOY": "DFL-COM-000002",
    "J03WPY": "DFL-COM-000002",
    "J03WQQ": "DFL-COM-000002",
    "J03WR9": "DFL-COM-000002",
}


def names(match_id, competition):
    return (
        "DFL_02_01_matchinformation_{}_DFL-MAT-{}.xml".format(competition, match_id),
        "DFL_04_03_positions_raw_observed_{}_DFL-MAT-{}.xml".format(competition, match_id),
    )


def download(name):
    destination = OUT / name
    if destination.is_file() and destination.stat().st_size:
        print("OK", name, "{:.1f} MB".format(destination.stat().st_size / 1e6))
        return
    temporary = destination.with_suffix(destination.suffix + ".part")
    with urlopen(BASE + name, timeout=120) as response, temporary.open("wb") as handle:
        while chunk := response.read(1 << 20):
            handle.write(chunk)
    temporary.replace(destination)
    print("OK", name, "{:.1f} MB".format(destination.stat().st_size / 1e6))


def main(argv):
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = argv or list(MATCHES)
    unknown = [match for match in wanted if match not in MATCHES]
    if unknown:
        print("Partidas desconhecidas: {}".format(", ".join(unknown)), file=sys.stderr)
        return 1
    for match_id in wanted:
        for name in names(match_id, MATCHES[match_id]):
            download(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
