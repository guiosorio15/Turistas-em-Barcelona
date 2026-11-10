"""CLI de checkout: integração reproduzível com a referência oficial."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "mtah"
SOURCES = {
    "tactical": (".mp4", "_atd.xml", "_atd.txt", "_homography.csv", "_smart_tagging.xml"),
    "broadcast": (".mp4", "_atd.xml", "_atd.txt", "_homography.csv"),
}


def data_root(value=None):
    return Path(value or os.environ.get("MTAH_DATA_DIR") or ROOT / "data").expanduser().resolve()


def expected_assets(folder, baseline_only=False):
    if baseline_only:
        return [folder / "tactical" / ("BAR-ATH_tactical" + suffix)
                for suffix in ("_atd.xml", "_atd.txt")]
    return [folder / source / ("BAR-ATH_" + source + suffix)
            for source, suffixes in SOURCES.items() for suffix in suffixes]


def missing_assets(folder, baseline_only=False):
    return [p for p in expected_assets(folder, baseline_only)
            if not p.is_file() or p.stat().st_size == 0]


def run_official(script, *args, env=None):
    subprocess.run([sys.executable, str(VENDOR / script), *map(str, args)],
                   cwd=VENDOR, env=env, check=True)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def code_hash():
    digest = hashlib.sha256()
    files = [ROOT / "pyproject.toml", ROOT / "uv.lock"]
    for folder in ("src", "scripts", "vendor", "configs"):
        files.extend(p for p in (ROOT / folder).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts
                     and p.suffix not in (".pyc", ".pyo"))
    for p in sorted(files):
        digest.update(p.relative_to(ROOT).as_posix().encode())
        digest.update(bytes.fromhex(sha256(p)))
    return digest.hexdigest()


def git_revision():
    result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                            text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else None


def load_config(path):
    with Path(path).open("rb") as handle:
        config = tomllib.load(handle)["baseline"]
    window = config["window"]
    if type(window) is not int or window < 0:
        raise ValueError("window deve ser um inteiro não negativo")
    name = config["submission_name"]
    if not isinstance(name, str) or not name or "/" in name or "\\" in name or not name.endswith(".csv"):
        raise ValueError("submission_name deve ser um nome simples terminado em .csv")
    return config


def reproduce(args):
    folder = data_root(args.data_dir)
    missing = missing_assets(folder, baseline_only=True)
    if missing:
        print("Tracking mínimo em falta:\n" + "\n".join(map(str, missing)), file=sys.stderr)
        return 1
    config_path = Path(args.config).resolve()
    config = load_config(config_path)
    destination = Path(args.output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, MTAH_DATA_DIR=str(folder))
    submission = destination / config["submission_name"]
    with tempfile.TemporaryDirectory(prefix="turistas-baseline-") as temporary:
        run_official("starter/baseline.py", "--window", config["window"], "--out", temporary, env=env)
        name = "baseline_raw.csv" if config["window"] == 0 else f"baseline_smooth{config['window']}.csv"
        shutil.copyfile(Path(temporary) / name, submission)
    run_official("evaluation/validate_submission.py", submission)
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "method": "official_nearest_player_majority_vote",
        "config": config,
        "config_sha256": sha256(config_path),
        "code_sha256": code_hash(),
        "git_commit": git_revision(),
        "python": sys.version,
        "dependencies": {name: version(name) for name in ("numpy", "pandas")},
        "inputs": {str(p.relative_to(folder)): sha256(p) for p in expected_assets(folder, True)},
        "submission": submission.name,
        "submission_sha256": sha256(submission),
    }
    manifest_path = submission.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Submissão: {submission}\nManifesto: {manifest_path}")
    return 0


def parser():
    cli = argparse.ArgumentParser(description="Turistas de la Nave — posse de bola reproduzível")
    commands = cli.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check-data", help="Verificar presença dos assets locais")
    check.add_argument("--data-dir")
    check.add_argument("--baseline-only", action="store_true")
    evaluate = commands.add_parser("evaluate", help="Avaliar CSVs com o scorer oficial público")
    evaluate.add_argument("--results", default=str(VENDOR / "evaluation/results"))
    evaluate.add_argument("--out", default=str(ROOT / "outputs/evaluation"))
    evaluate.add_argument("--bootstrap", type=int, default=0)
    validate = commands.add_parser("validate", help="Validar um CSV no contrato oficial")
    validate.add_argument("csv")
    build = commands.add_parser("reproduce", help="Gerar a baseline e manifesto a partir de tracking")
    build.add_argument("--data-dir")
    build.add_argument("--config", default=str(ROOT / "configs/baseline.toml"))
    build.add_argument("--output-dir", default=str(ROOT / "outputs/submissions"))
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "check-data":
            folder = data_root(args.data_dir)
            missing = missing_assets(folder, args.baseline_only)
            for path in expected_assets(folder, args.baseline_only):
                print(f"{'FALTA' if path in missing else 'OK'} {path}")
            return 1 if missing else 0
        if args.command == "validate":
            run_official("evaluation/validate_submission.py", Path(args.csv).resolve())
        elif args.command == "evaluate":
            gt = VENDOR / "evaluation/gt/BAR-ATH_possession_gt_public.csv"
            results = Path(args.results).resolve()
            run_official("evaluation/run_evaluation.py",
                         "--gt", os.path.relpath(gt, VENDOR),
                         "--results", os.path.relpath(results, VENDOR),
                         "--out", Path(args.out).resolve(),
                         "--bootstrap", args.bootstrap, "--no-detail")
        else:
            return reproduce(args)
        return 0
    except subprocess.CalledProcessError as error:
        return error.returncode
    except (OSError, ValueError, KeyError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
