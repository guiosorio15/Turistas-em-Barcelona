"""Treina o modelo final em DFL e guarda o artefacto.

O jogo fornecido não entra no treino. O artefacto guarda features, classes,
custos de transição e a proveniência dos dados.

Uso:
    uv run --locked --extra notebooks python scripts/train_model.py
    uv run --locked --extra notebooks python scripts/train_model.py --matches J03WMX,J03WN1
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from run_e1 import cached_dataset
from run_lomo import match_ids

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", default="")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--turnover", type=float, default=9.0)
    parser.add_argument("--dead", type=float, default=12.0)
    parser.add_argument("--output", default=str(ROOT / "models/e1_dfl_v3.joblib"))
    args = parser.parse_args(argv)

    available = match_ids()
    wanted = [item.strip() for item in args.matches.split(",") if item.strip()]
    matches = [match for match in available if not wanted or match in wanted]
    if not matches:
        raise SystemExit("Sem jogos DFL; correr scripts/fetch_dfl.py")

    datasets = {match: cached_dataset(match, degrade=not args.clean, seed=args.seed)
                for match in matches}
    train = pd.concat(datasets.values(), ignore_index=True)
    excluded = {"label", "period", "restart",
                "p90_speed", "p90_speed_ma13", "p90_speed_ma45"}
    features = [column for column in train.columns if column not in excluded]
    model = HistGradientBoostingClassifier(
        max_iter=args.iterations, learning_rate=0.08, max_leaf_nodes=31,
        l2_regularization=1.0, random_state=0, early_stopping=False,
    )
    model.fit(train[features], train["label"])

    artifact = {
        "model": model,
        "features": features,
        "classes": model.classes_.astype(int).tolist(),
        "turnover": args.turnover,
        "dead": args.dead,
        "matches": matches,
        "degraded": not args.clean,
        "seed": args.seed,
        "rows": int(len(train)),
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, output)
    print(json.dumps({
        "output": str(output),
        "matches": matches,
        "degraded": not args.clean,
        "rows": int(len(train)),
        "features": len(features),
        "classes": artifact["classes"],
        "cost": {"turnover": args.turnover, "dead": args.dead},
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
