"""Leave-one-match-out em DFL para o primeiro modelo (E1/E2).

Treino e validação exclusivamente em DFL. O jogo fornecido não entra aqui.

Uso:
    uv sync --locked --extra notebooks
    uv run --locked --extra notebooks python scripts/run_lomo.py --degrade
    uv run --locked --extra notebooks python scripts/run_lomo.py --matches J03WMX,J03WN1,J03WOH
"""
from __future__ import annotations

import argparse
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from run_e1 import (A, D, DFL_DIR, H, X, cached_dataset, load_metrics, metrics,
                    viterbi)


def match_ids():
    return sorted(path.stem.rsplit("-", 1)[-1]
                  for path in DFL_DIR.glob("*positions_raw_observed_*.xml"))


def join_periods(parts):
    output = []
    for part in parts:
        output.extend(np.asarray(part, dtype=np.int8).tolist())
        output.append(X)
    return np.asarray(output[:-1], dtype=np.int8)


def evaluate_match(pm, data, model, features, turnover, dead):
    cost = np.array([[0.0, turnover, dead],
                     [turnover, 0.0, dead],
                     [dead, dead, 0.0]], dtype=np.float32)
    truth_parts, prediction_parts = [], []
    for _, group in data.groupby("period", sort=True):
        probability = model.predict_proba(group[features])
        logp = np.log(np.clip(probability, 1e-9, 1.0))
        truth_parts.append(group["label"].to_numpy(dtype=np.int8))
        prediction_parts.append(viterbi(logp, cost))
    truth = join_periods(truth_parts)
    prediction = join_periods(prediction_parts)
    return metrics(pm, truth, prediction)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", default="")
    parser.add_argument("--degrade", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--turnover", type=float, default=9.0)
    parser.add_argument("--dead", type=float, default=12.0)
    parser.add_argument("--max-train-rows", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=250)
    args = parser.parse_args(argv)

    available = match_ids()
    wanted = [item.strip() for item in args.matches.split(",") if item.strip()]
    matches = [match for match in available if not wanted or match in wanted]
    if len(matches) < 2:
        raise SystemExit("São necessários pelo menos dois jogos; tenho {}".format(available))

    print("A preparar features: {}".format(", ".join(matches)))
    datasets = {match: cached_dataset(match, degrade=args.degrade, seed=args.seed)
                for match in matches}
    excluded = {"label", "period", "restart",
                "p90_speed", "p90_speed_ma13", "p90_speed_ma45"}
    features = [column for column in datasets[matches[0]].columns
                if column not in excluded]
    pm = load_metrics()
    folds = {}

    for test_match in matches:
        train = pd.concat([datasets[match] for match in matches if match != test_match],
                          ignore_index=True)
        if args.max_train_rows and len(train) > args.max_train_rows:
            train = train.sample(n=args.max_train_rows, random_state=0)
        model = HistGradientBoostingClassifier(
            max_iter=args.iterations, learning_rate=0.08, max_leaf_nodes=31,
            l2_regularization=1.0, random_state=0, early_stopping=False,
        )
        model.fit(train[features], train["label"])
        result = evaluate_match(pm, datasets[test_match], model, features,
                                args.turnover, args.dead)
        folds[test_match] = result
        print("{}: spellF1 {:.4f}  macroF1 {:.4f}  posses {}/{}".format(
            test_match, result["spell_f1_mean"], result["macro_f1"],
            result["n_pred_spells"], result["n_gt_spells"]))

    spell = [result["spell_f1_mean"] for result in folds.values()]
    macro = [result["macro_f1"] for result in folds.values()]
    report = {
        "degraded": args.degrade,
        "seed": args.seed,
        "matches": matches,
        "folds": folds,
        "mean_spell_f1": float(np.mean(spell)),
        "std_spell_f1": float(np.std(spell)),
        "mean_macro_f1": float(np.mean(macro)),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
