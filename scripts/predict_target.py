"""Gera uma submissão do jogo alvo a partir do ATD tático e de um modelo DFL.

O algoritmo não é treinado no jogo fornecido. A saída é `X` fora das duas
partes avaliadas e `H/A/D` dentro delas.

Uso:
    uv run --locked --extra notebooks python scripts/predict_target.py \
        --model outputs/models/e1_dfl.joblib
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "vendor" / "mtah"))

from games import half_video_blocks, source_frames  # noqa: E402
from turistas.atd import load  # noqa: E402
from turistas.cli import code_hash, git_revision, sha256  # noqa: E402
from run_e1 import D, H, X, period_features, viterbi  # noqa: E402


def goalkeeper_flip(atd, start, stop, home_slots):
    """Decide se a casa ataca +x, pelo slot mais próximo de uma baliza."""
    x = atd.players[start:stop, home_slots, 0]
    near = ((x < 0.08) | (x > 0.92)).mean(axis=0)
    index = int(np.argmax(near))
    goalkeeper = int(home_slots[index])
    mean_x = float(np.nanmean(atd.players[start:stop, goalkeeper, 0]))
    return mean_x > 0.5, goalkeeper, float(near[index])


def half_frame(atd, start, stop):
    data = {
        "ball_x": atd.ball[start:stop, 0],
        "ball_y": atd.ball[start:stop, 1],
        "ball_speed": atd.ball[start:stop, 2],
    }
    for slot in range(atd.players.shape[1]):
        data["s{}_x".format(slot)] = atd.players[start:stop, slot, 0]
        data["s{}_y".format(slot)] = atd.players[start:stop, slot, 1]
        data["s{}_s".format(slot)] = atd.players[start:stop, slot, 2]
    return pd.DataFrame(data)


def prediction(artifact, features):
    model = artifact["model"]
    probability = model.predict_proba(features[artifact["features"]])
    logp = np.full((len(features), 3), -np.inf, dtype=np.float64)
    logp[:, artifact["classes"]] = np.log(np.clip(probability, 1e-9, 1.0))
    cost = np.array([[0.0, artifact["turnover"], artifact["dead"]],
                     [artifact["turnover"], 0.0, artifact["dead"]],
                     [artifact["dead"], artifact["dead"], 0.0]], dtype=np.float32)
    return viterbi(logp, cost)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=str(ROOT / "models/e1_dfl_v3.joblib"))
    parser.add_argument("--xml", default=str(ROOT / "data/tactical/BAR-ATH_tactical_atd.xml"))
    parser.add_argument("--txt", default=str(ROOT / "data/tactical/BAR-ATH_tactical_atd.txt"))
    parser.add_argument("--cache", default=str(ROOT / "data/tactical/atd.npz"))
    parser.add_argument("--output",
                        default=str(ROOT / "outputs/submissions/Turistas_de_la_Nave_model.csv"))
    args = parser.parse_args(argv)

    artifact = joblib.load(args.model)
    atd = load(args.xml, args.txt, cache=args.cache)
    home_slots = np.flatnonzero(atd.team_of == 0)
    away_slots = np.flatnonzero(atd.team_of == 1)
    home_ids = ["s{}".format(slot) for slot in home_slots]
    away_ids = ["s{}".format(slot) for slot in away_slots]

    labels = np.full(source_frames("tactical"), "X", dtype="<U1")
    halves = []
    for half, first, last in half_video_blocks("BAR-ATH"):
        start, stop = first, last + 1
        flip, goalkeeper, fraction = goalkeeper_flip(atd, start, stop, home_slots)
        features = period_features(half_frame(atd, start, stop), home_ids, away_ids, flip)
        path = prediction(artifact, features)
        labels[start:stop] = np.array(["H", "A", "D"])[path]
        halves.append({
            "half": half, "frames": int(stop - start), "flip": bool(flip),
            "goalkeeper_slot": int(goalkeeper), "gk_near_goal_fraction": round(fraction, 3),
        })

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"frame": np.arange(len(labels)), "label": labels}).to_csv(output, index=False)
    counts = {label: int((labels == label).sum()) for label in ("H", "A", "D", "X")}
    alive = (labels == "H") | (labels == "A")
    spells = int(np.sum(alive[1:] & (labels[1:] != labels[:-1]))) + int(alive[0])
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "method": "dfl_gbm3_viterbi3",
        "model": str(Path(args.model)),
        "model_sha256": sha256(args.model),
        "config": {
            "matches": artifact["matches"],
            "degraded": artifact["degraded"],
            "seed": artifact["seed"],
            "training_rows": artifact["rows"],
            "features": len(artifact["features"]),
            "classes": artifact["classes"],
            "turnover": artifact["turnover"],
            "dead": artifact["dead"],
        },
        "code_sha256": code_hash(),
        "git_commit": git_revision(),
        "inputs": {"tactical_atd_xml": sha256(args.xml),
                   "tactical_atd_txt": sha256(args.txt)},
        "submission": output.name,
        "submission_sha256": sha256(output),
        "labels": counts,
        "possessions": spells,
        "halves": halves,
    }
    manifest_path = output.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "output": str(output),
        "manifest": str(manifest_path),
        "rows": int(len(labels)),
        "labels": counts,
        "possessions": spells,
        "halves": halves,
        "model": {"matches": artifact["matches"], "degraded": artifact["degraded"],
                  "cost": {"turnover": artifact["turnover"], "dead": artifact["dead"]}},
    }, indent=2, ensure_ascii=False))

    subprocess.run([sys.executable, str(ROOT / "vendor/mtah/evaluation/validate_submission.py"),
                    str(output)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
