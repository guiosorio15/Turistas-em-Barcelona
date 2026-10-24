"""Executar após uv sync: uv run --locked python scripts/check_data.py."""
import sys
from turistas.cli import main

raise SystemExit(main(["check-data", *sys.argv[1:]]))
