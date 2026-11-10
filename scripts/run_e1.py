"""E1/E2: primeiro modelo aprendido em DFL.

Treino e validação só em DFL (dados externos, CC-BY 4.0). O jogo fornecido nunca
entra neste script. O objetivo é medir, não escolher variantes no público.

Uso:
    uv sync --locked --extra notebooks
    uv run --locked --extra notebooks python scripts/run_e1.py --match J03WMX
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

ROOT = Path(__file__).resolve().parents[1]
DFL_DIR = ROOT / "data" / "dfl"
PITCH_LENGTH, PITCH_WIDTH = 105.3, 68.0
H, A, D, X = 0, 1, 2, 3
FEATURES = ("d1", "d1_now", "d2", "n2", "n5", "n10", "n_present", "cx", "cy",
            "ball_dx", "ball_dy", "spread", "depth", "width", "mean_speed",
            "still", "pressure", "ball_dist")


def load_metrics():
    """Carrega o scorer oficial sem copiar nem alterar uma linha."""
    path = ROOT / "vendor/mtah/evaluation/possession_metrics.py"
    spec = importlib.util.spec_from_file_location("possession_metrics", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_meta(path):
    root = ET.parse(path).getroot()
    teams = {team.get("TeamId"): team.get("Role") for team in root.iter("Team")}
    home_id = next(team_id for team_id, role in teams.items() if role == "home")
    away_id = next(team_id for team_id, role in teams.items() if role == "guest")
    players = {}
    for team in root.iter("Team"):
        for player in team.iter("Player"):
            players[player.get("PersonId")] = (team.get("TeamId"), player.get("PlayingPosition"))
    return home_id, away_id, players


def load_match(match_id):
    meta_path = next(DFL_DIR.glob("*matchinformation*{}*.xml".format(match_id)))
    cache = DFL_DIR / "{}.pkl.gz".format(match_id)
    if cache.is_file():
        frame = pd.read_pickle(cache)
    else:
        from kloppy import sportec
        raw_path = next(DFL_DIR.glob("*positions_raw*{}*.xml".format(match_id)))
        frame = sportec.load_tracking(
            meta_data=str(meta_path), raw_data=str(raw_path), only_alive=False
        ).to_df()
        frame.to_pickle(cache, compression="gzip")
    return frame, *parse_meta(meta_path)


def team_columns(frame, players, team_id):
    return [player_id for player_id in players
            if players[player_id][0] == team_id and player_id + "_x" in frame.columns]


def flip_flags(frame, players, home_id):
    """True where a meia tem de ser espelhada para a casa atacar +x."""
    goalkeepers = [player_id for player_id, (team_id, position) in players.items()
                   if team_id == home_id and position == "TW"
                   and player_id + "_x" in frame.columns]
    flags = {}
    for period, group in frame.groupby("period_id", sort=True):
        if goalkeepers:
            flags[period] = bool(group[[g + "_x" for g in goalkeepers]].to_numpy().mean() > 0.5)
        else:
            flags[period] = False
    return flags


def team_arrays(group, ids, flip, rng=None, player_fraction=0.0, speed_scale=1.0):
    x = group[[player_id + "_x" for player_id in ids]].to_numpy(dtype=np.float32).copy()
    y = group[[player_id + "_y" for player_id in ids]].to_numpy(dtype=np.float32).copy()
    speed = group[[player_id + "_s" for player_id in ids]].to_numpy(dtype=np.float32).copy()
    x *= PITCH_LENGTH
    y *= PITCH_WIDTH
    speed *= speed_scale
    if rng is not None:
        x += rng.normal(0.0, 0.2, x.shape).astype(np.float32)
        y += rng.normal(0.0, 0.2, y.shape).astype(np.float32)
        if player_fraction:
            missing = rng.random(x.shape) < player_fraction
            x[missing] = np.nan
            y[missing] = np.nan
            speed[missing] = np.nan
    if flip:
        x = PITCH_LENGTH - x
    return x, y, speed


def degrade_ball(ball_x, ball_y, rng, fraction=0.41, min_gap=75, max_gap=750):
    """Mascara 41% da bola em blocos longos, como no tracker do jogo."""
    length = len(ball_x)
    mask = np.zeros(length, dtype=bool)
    target = int(round(length * fraction))
    while mask.sum() < target:
        gap = int(rng.integers(min_gap, max_gap + 1))
        if gap >= length:
            break
        start = int(rng.integers(0, length - gap + 1))
        mask[start:start + gap] = True
    ball_x = ball_x.copy()
    ball_y = ball_y.copy()
    ball_x[mask] = np.nan
    ball_y[mask] = np.nan
    return ball_x, ball_y


def visibility(visible):
    series = pd.Series(visible)
    group = (~series).cumsum()
    since = np.where(series, 0, series.groupby(group).cumcount().to_numpy() + 1)
    reverse = series[::-1]
    reverse_group = (~reverse).cumsum()
    until = np.where(reverse, 0, reverse.groupby(reverse_group).cumcount().to_numpy() + 1)[::-1]
    gap = np.where(series, 0, series.groupby(group).transform("size").to_numpy())
    return since.astype(np.float32), until.astype(np.float32), gap.astype(np.float32)


def fit_models(train, test, features, three=False, iterations=300):
    params = dict(max_iter=iterations, learning_rate=0.08, max_leaf_nodes=31,
                  l2_regularization=1.0, random_state=0, early_stopping=False)
    if not three:
        model = HistGradientBoostingClassifier(**params)
        model.fit(train[features], train["label"])
        probability = model.predict_proba(test[features])
        classes = model.classes_.astype(np.int8)
        return np.log(np.clip(probability, 1e-9, 1.0)), probability, classes

    alive = HistGradientBoostingClassifier(**params)
    alive.fit(train[features], (train["label"] != D).astype(np.int8))
    owner_train = train[train["label"] != D]
    owner = HistGradientBoostingClassifier(**params)
    owner.fit(owner_train[features], (owner_train["label"] == H).astype(np.int8))
    p_alive = alive.predict_proba(test[features])[:, list(alive.classes_).index(1)]
    p_owner = owner.predict_proba(test[features])[:, list(owner.classes_).index(1)]
    p_alive = np.clip(p_alive, 1e-9, 1.0 - 1e-9)
    p_owner = np.clip(p_owner, 1e-9, 1.0 - 1e-9)
    logp = np.column_stack([
        np.log(p_alive) + np.log(p_owner),
        np.log(p_alive) + np.log1p(-p_owner),
        np.log1p(-p_alive),
    ])
    return logp, np.exp(logp), np.array([H, A, D], dtype=np.int8)


def fit_models_four(train, test, features, iterations=300):
    """Três classes + classificador de quem recomeça; devolve log-probs de 4 estados."""
    params = dict(max_iter=iterations, learning_rate=0.08, max_leaf_nodes=31,
                  l2_regularization=1.0, random_state=0, early_stopping=False)
    model = HistGradientBoostingClassifier(**params)
    model.fit(train[features], train["label"])
    probability = model.predict_proba(test[features])
    classes = model.classes_.astype(np.int8)
    three = np.zeros((len(test), 3), dtype=np.float64)
    three[:, classes] = probability

    dead_train = train[train["restart"] >= 0]
    restart = HistGradientBoostingClassifier(**params)
    restart.fit(dead_train[features], dead_train["restart"].astype(np.int8))
    p_restart = restart.predict_proba(test[features])[:, list(restart.classes_).index(1)]
    p_restart = np.clip(p_restart, 1e-9, 1.0 - 1e-9)
    p_dead = np.clip(three[:, D], 1e-9, 1.0)
    logp = np.column_stack([
        np.log(np.clip(three[:, H], 1e-9, 1.0)),
        np.log(np.clip(three[:, A], 1e-9, 1.0)),
        np.log(p_dead) + np.log(p_restart),
        np.log(p_dead) + np.log1p(-p_restart),
    ])
    return logp, three, classes


def dead_stage(features, penalty=14.0):
    """Etapa física de bola morta, inspirada em Suleyman (2026).

    Usa p90 da velocidade coletiva, bola fora, lacuna longa e isolamento.
    Devolve uma máscara booleana de frames mortos.
    """
    speed = features["p90_speed_ma45"].to_numpy(dtype=np.float64)
    speed = np.nan_to_num(speed, nan=2.5)
    ball_x = features["ball_x"].ffill().bfill().fillna(PITCH_LENGTH / 2).to_numpy()
    ball_y = features["ball_y"].ffill().bfill().fillna(PITCH_WIDTH / 2).to_numpy()
    ball_speed = features["ball_speed"].to_numpy(dtype=np.float64)
    nearest = np.fmin(features["h_d1"].to_numpy(dtype=np.float64),
                      features["a_d1"].to_numpy(dtype=np.float64))
    gap = features["ball_gap"].to_numpy(dtype=np.float64)

    low = np.clip((2.08 - speed) / 0.30, -2.2, 2.6)
    live = np.isfinite(ball_speed) & (ball_speed > 4.8) & (nearest < 2.8)
    low = np.where(live, -2.0, low)
    outside = ((ball_x < 0.0) | (ball_x > PITCH_LENGTH)
               | (ball_y < 0.0) | (ball_y > PITCH_WIDTH))
    score = (low + 3.8 * outside
             + 2.6 * ((gap >= 60) & (speed < 2.20))
             + 1.8 * ((nearest > 4.5) & (speed < 2.20)))
    logp = np.column_stack([np.zeros(len(score)), score])
    cost = np.array([[0.0, penalty], [penalty, 0.0]], dtype=np.float32)
    return viterbi(logp, cost).astype(bool)


def ball_out_mask(features, confirmation=3):
    """Frames em que a bola está fora do polígono do campo.

    Usa a última posição conhecida quando a bola falta. Exige `confirmation`
    frames consecutivos para não reagir a ruído de tracking.
    """
    ball_x = features["ball_x"].ffill().bfill().fillna(PITCH_LENGTH / 2).to_numpy()
    ball_y = features["ball_y"].ffill().bfill().fillna(PITCH_WIDTH / 2).to_numpy()
    raw = ((ball_x < 0.0) | (ball_x > PITCH_LENGTH)
           | (ball_y < 0.0) | (ball_y > PITCH_WIDTH))
    if confirmation <= 1:
        return raw
    out = (pd.Series(raw).rolling(confirmation, min_periods=confirmation).sum()
           >= confirmation)
    return out.fillna(False).to_numpy()


def apply_ball_out(path, features, confirmation=3):
    out = ball_out_mask(features, confirmation)
    result = path.copy()
    result[out] = D
    return result


def team_features(x, y, speed, ball_x, ball_y):
    dx = x - ball_x[:, None]
    dy = y - ball_y[:, None]
    distance = np.sqrt(dx * dx + dy * dy)
    ordered = np.sort(distance, axis=1)
    count = ordered.shape[1]
    d1 = ordered[:, 0] if count else np.full(len(x), np.nan, dtype=np.float32)
    d2 = ordered[:, 1] if count > 1 else np.full(len(x), np.nan, dtype=np.float32)
    centroid_x = np.nanmean(x, axis=1)
    centroid_y = np.nanmean(y, axis=1)
    spread = np.sqrt(np.nanvar(x, axis=1) + np.nanvar(y, axis=1))
    depth = np.nanpercentile(x, 90, axis=1) - np.nanpercentile(x, 10, axis=1)
    width = np.nanpercentile(y, 90, axis=1) - np.nanpercentile(y, 10, axis=1)
    return {
        "d1": d1.astype(np.float32),
        "d2": d2.astype(np.float32),
        "n2": np.sum(distance < 2, axis=1).astype(np.float32),
        "n5": np.sum(distance < 5, axis=1).astype(np.float32),
        "n10": np.sum(distance < 10, axis=1).astype(np.float32),
        "n_present": np.minimum(np.sum(np.isfinite(x), axis=1), 11).astype(np.float32),
        "cx": centroid_x.astype(np.float32),
        "cy": centroid_y.astype(np.float32),
        "ball_dx": (centroid_x - ball_x).astype(np.float32),
        "ball_dy": (centroid_y - ball_y).astype(np.float32),
        "spread": spread.astype(np.float32),
        "depth": depth.astype(np.float32),
        "width": width.astype(np.float32),
        "mean_speed": np.nanmean(speed, axis=1).astype(np.float32),
        "still": np.nanmean(speed < 1.0, axis=1).astype(np.float32),
        "ball_dist": np.sqrt((centroid_x - ball_x) ** 2 + (centroid_y - ball_y) ** 2).astype(np.float32),
    }


def pressure(x, y, opponent_x, opponent_y, chunk=20000):
    """Média de adversários a menos de 10 m de cada jogador presente."""
    out = np.empty(len(x), dtype=np.float32)
    for start in range(0, len(x), chunk):
        stop = min(start + chunk, len(x))
        dx = x[start:stop, :, None] - opponent_x[start:stop, None, :]
        dy = y[start:stop, :, None] - opponent_y[start:stop, None, :]
        distance = np.sqrt(dx * dx + dy * dy)
        present = np.isfinite(x[start:stop, :, None]) & np.isfinite(opponent_x[start:stop, None, :])
        counts = np.where(present, distance < 10, np.nan)
        out[start:stop] = np.nanmean(counts, axis=(1, 2))
    return out


def rolling_mean(values, window):
    return pd.Series(values).rolling(window, center=True, min_periods=1).mean().to_numpy(dtype=np.float32)


def period_features(group, home_ids, away_ids, flip, rng=None, degrade=False, speed_scale=1.0):
    ball_x = group["ball_x"].to_numpy(dtype=np.float32) * PITCH_LENGTH
    ball_y = group["ball_y"].to_numpy(dtype=np.float32) * PITCH_WIDTH
    if flip:
        ball_x = PITCH_LENGTH - ball_x
    if degrade:
        ball_x, ball_y = degrade_ball(ball_x, ball_y, rng)
        ball_x += rng.normal(0.0, 0.2, len(ball_x)).astype(np.float32)
        ball_y += rng.normal(0.0, 0.2, len(ball_y)).astype(np.float32)
    visible = np.isfinite(ball_x) & np.isfinite(ball_y)
    filled_x = pd.Series(ball_x).ffill().bfill().fillna(PITCH_LENGTH / 2).to_numpy(dtype=np.float32)
    filled_y = pd.Series(ball_y).ffill().bfill().fillna(PITCH_WIDTH / 2).to_numpy(dtype=np.float32)
    since, until, gap = visibility(visible)

    player_rng = rng if degrade else None
    player_fraction = 0.05 if degrade else 0.0
    home_x, home_y, home_speed = team_arrays(
        group, home_ids, flip, player_rng, player_fraction, speed_scale)
    away_x, away_y, away_speed = team_arrays(
        group, away_ids, flip, player_rng, player_fraction, speed_scale)
    home = team_features(home_x, home_y, home_speed, filled_x, filled_y)
    away = team_features(PITCH_LENGTH - away_x, away_y, away_speed,
                         PITCH_LENGTH - filled_x, filled_y)
    home["pressure"] = pressure(home_x, home_y, away_x, away_y)
    away["pressure"] = pressure(away_x, away_y, home_x, home_y)
    home["d1_now"] = np.where(visible, home["d1"], np.nan).astype(np.float32)
    away["d1_now"] = np.where(visible, away["d1"], np.nan).astype(np.float32)
    all_speed = np.concatenate([home_speed, away_speed], axis=1)
    p90_speed = np.nanpercentile(all_speed, 90, axis=1)
    p90_speed = np.clip(p90_speed, 0.0, 12.0)

    velocity_x = np.diff(filled_x, prepend=filled_x[:1]) * 25.0
    velocity_y = np.diff(filled_y, prepend=filled_y[:1]) * 25.0
    raw_speed = np.sqrt(velocity_x * velocity_x + velocity_y * velocity_y)
    valid = visible & (raw_speed <= 40.0)
    speed = np.where(valid, raw_speed, np.nan)
    speed = pd.Series(speed).rolling(5, center=True, min_periods=1).median().to_numpy(dtype=np.float32)
    acceleration = np.diff(speed, prepend=speed[:1]) * 25.0
    acceleration = np.where(np.abs(acceleration) <= 20.0, acceleration, np.nan)

    data = {
        "ball_x": ball_x.astype(np.float32),
        "ball_y": ball_y.astype(np.float32),
        "ball_visible": visible.astype(np.float32),
        "ball_since": since,
        "ball_until": until,
        "ball_gap": gap,
        "ball_speed": speed,
        "ball_accel": acceleration.astype(np.float32),
        "p90_speed": p90_speed.astype(np.float32),
    }
    for prefix, values in (("h", home), ("a", away)):
        for name, array in values.items():
            data["{}_{}".format(prefix, name)] = array
    for name in FEATURES:
        data["diff_{}".format(name)] = (home[name] - away[name]).astype(np.float32)
    for name in ("d1", "d1_now", "cx", "depth", "width", "pressure", "n_present", "still"):
        for window in (25, 50):
            data["h_{}_ma{}".format(name, window)] = rolling_mean(home[name], window)
            data["a_{}_ma{}".format(name, window)] = rolling_mean(away[name], window)
            data["diff_{}_ma{}".format(name, window)] = (
                data["h_{}_ma{}".format(name, window)] - data["a_{}_ma{}".format(name, window)]
            )
    for window in (25, 50, 125):
        data["ball_visible_ma{}".format(window)] = rolling_mean(
            visible.astype(np.float32), window
        )
        data["ball_still_ma{}".format(window)] = rolling_mean(
            np.where(valid, (speed < 0.5).astype(np.float32), np.nan), window
        )
    for lag in (25, 100):
        previous_x = np.concatenate([np.full(lag, np.nan, dtype=np.float32), filled_x[:-lag]])
        previous_y = np.concatenate([np.full(lag, np.nan, dtype=np.float32), filled_y[:-lag]])
        data["ball_disp_{}".format(lag)] = np.sqrt(
            (filled_x - previous_x) ** 2 + (filled_y - previous_y) ** 2
        ).astype(np.float32)
    data["ball_vx"] = np.where(valid, velocity_x, np.nan).astype(np.float32)
    data["ball_vy"] = np.where(valid, velocity_y, np.nan).astype(np.float32)
    data["ball_vx_ma5"] = rolling_mean(data["ball_vx"], 5)
    data["ball_vy_ma5"] = rolling_mean(data["ball_vy"], 5)
    data["ball_speed_ma25"] = rolling_mean(speed, 25)
    data["p90_speed_ma13"] = rolling_mean(p90_speed, 13)
    data["p90_speed_ma45"] = rolling_mean(p90_speed, 45)
    return pd.DataFrame(data)


def dataset(frame, home_id, away_id, players, degrade=False, seed=0):
    flips = flip_flags(frame, players, home_id)
    home_ids = team_columns(frame, players, home_id)
    away_ids = team_columns(frame, players, away_id)
    parts = []
    for period, group in frame.groupby("period_id", sort=True):
        rng = np.random.default_rng(seed + int(period)) if degrade else None
        features = period_features(group, home_ids, away_ids, flips[period],
                                   rng=rng, degrade=degrade, speed_scale=1.0 / 3.6)
        dead = group["ball_state"].eq("dead").to_numpy()
        home = group["ball_owning_team_id"].eq(home_id).to_numpy()
        features["label"] = np.where(dead, D, np.where(home, H, A)).astype(np.int8)
        features["restart"] = np.where(dead, home.astype(np.int8), -1)
        features["period"] = period
        parts.append(features)
    return pd.concat(parts, ignore_index=True)


def cached_dataset(match_id, degrade=False, seed=0):
    cache_dir = DFL_DIR / "features"
    cache = cache_dir / "{}_{}_{}_v5.pkl.gz".format(match_id, "deg" if degrade else "clean", seed)
    if cache.is_file():
        return pd.read_pickle(cache)
    frame, home_id, away_id, players = load_match(match_id)
    data = dataset(frame, home_id, away_id, players, degrade=degrade, seed=seed)
    cache_dir.mkdir(parents=True, exist_ok=True)
    data.to_pickle(cache, compression="gzip")
    return data


def viterbi(logp, cost):
    length, states = logp.shape
    score = np.empty_like(logp)
    back = np.empty((length, states), dtype=np.int8)
    score[0] = logp[0]
    for index in range(1, length):
        candidates = score[index - 1][:, None] - cost
        back[index] = np.argmax(candidates, axis=0)
        score[index] = logp[index] + candidates[back[index], np.arange(states)]
    path = np.empty(length, dtype=np.int8)
    path[-1] = np.argmax(score[-1])
    for index in range(length - 1, 0, -1):
        path[index - 1] = back[index, path[index]]
    return path


def metrics(pm, truth, prediction):
    result = pm.evaluate(truth, prediction)
    keys = ("macro_f1", "spell_f1_mean", "n_gt_spells", "n_pred_spells",
            "mean_spell_duration_s", "fragmentation", "n_graded", "alive_dead_f1")
    return {key: result[key] for key in keys}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--match", default="J03WMX")
    parser.add_argument("--train-period", type=int, default=1)
    parser.add_argument("--test-period", type=int, default=2)
    parser.add_argument("--turnover", type=float, default=9.0)
    parser.add_argument("--dead", type=float, default=12.0)
    parser.add_argument("--degrade", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--ball-out", action="store_true")
    parser.add_argument("--ball-out-confirmation", type=int, default=3)
    parser.add_argument("--three-classifiers", action="store_true")
    parser.add_argument("--four-state", action="store_true")
    parser.add_argument("--restart-cost", type=float, default=1.0)
    parser.add_argument("--dead-stage", action="store_true")
    parser.add_argument("--dead-stage-penalty", type=float, default=14.0)
    args = parser.parse_args(argv)

    frame, home_id, away_id, players = load_match(args.match)
    data = dataset(frame, home_id, away_id, players, degrade=args.degrade, seed=args.seed)
    excluded = {"label", "period", "restart",
                "p90_speed", "p90_speed_ma13", "p90_speed_ma45"}
    feature_columns = [column for column in data.columns if column not in excluded]
    train = data[data["period"] == args.train_period]
    test = data[data["period"] == args.test_period]

    if args.four_state:
        logp, probability, classes = fit_models_four(train, test, feature_columns, 300)
    else:
        logp, probability, classes = fit_models(
            train, test, feature_columns, three=args.three_classifiers, iterations=300
        )
    truth = test["label"].to_numpy(dtype=np.int8)
    argmax = classes[np.argmax(probability, axis=1)]
    if args.four_state:
        big = 1e6
        cost = np.array([[0.0, args.turnover, args.dead, args.dead],
                         [args.turnover, 0.0, args.dead, args.dead],
                         [args.dead, big, 0.0, args.restart_cost],
                         [big, args.dead, args.restart_cost, 0.0]], dtype=np.float32)
        decoded_four = viterbi(logp, cost)
        decoded = np.where(decoded_four >= 2, D, decoded_four).astype(np.int8)
    else:
        cost = np.array([[0.0, args.turnover, args.dead],
                         [args.turnover, 0.0, args.dead],
                         [args.dead, args.dead, 0.0]], dtype=np.float32)
        decoded = viterbi(logp, cost)

    pm = load_metrics()
    report = {
        "match": args.match,
        "train_period": args.train_period,
        "test_period": args.test_period,
        "degraded": args.degrade,
        "seed": args.seed,
        "rows": {"train": int(len(train)), "test": int(len(test))},
        "features": len(feature_columns),
        "model_type": ("four_state" if args.four_state
                       else "three_classifiers" if args.three_classifiers else "single"),
        "label_counts_test": {name: int((truth == code).sum())
                              for name, code in (("H", H), ("A", A), ("D", D))},
        "argmax": metrics(pm, truth, argmax),
        "viterbi": metrics(pm, truth, decoded),
        "cost": {"turnover": args.turnover, "dead": args.dead,
                 "restart": args.restart_cost, "states": 4 if args.four_state else 3},
    }
    if args.ball_out:
        rule = apply_ball_out(decoded, test, args.ball_out_confirmation)
        report["viterbi_ball_out"] = metrics(pm, truth, rule)
        report["ball_out"] = {
            "confirmation": args.ball_out_confirmation,
            "frames": int(ball_out_mask(test, args.ball_out_confirmation).sum()),
        }
    if args.dead_stage:
        dead = dead_stage(test, args.dead_stage_penalty)
        staged = decoded.copy()
        staged[dead] = D
        report["viterbi_dead_stage"] = metrics(pm, truth, staged)
        report["dead_stage"] = {
            "penalty": args.dead_stage_penalty,
            "frames": int(dead.sum()),
        }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
