"""Executar após uv sync: uv run --locked python scripts/reproduce.py."""
import sys
from turistas.cli import main

raise SystemExit(main(["reproduce", *sys.argv[1:]]))
