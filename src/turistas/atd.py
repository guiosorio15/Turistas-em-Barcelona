"""Leitura do ATD tático fornecido (FIFA/EPTS) e cache local.

O raw tem uma linha por frame:
    frame_id:slot_0;slot_1;...:ball
cada grupo é "x,y,speed" em coordenadas normalizadas, ou NaN quando ausente.
O vídeo tático é a autoridade dos frames; o raw conta a partir de 1.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np


@dataclass(frozen=True)
class ATD:
    players: np.ndarray  # (frames, slots, 3): x, y, speed
    ball: np.ndarray     # (frames, 3): x, y, speed
    team_of: np.ndarray  # (slots,): 0 casa, 1 fora
    team_ids: tuple[str, str]
    team_names: tuple[str, str]


def parse_meta(path):
    root = ET.parse(path).getroot()
    teams = list(root.iter("Team"))
    if len(teams) != 2:
        raise ValueError("esperava 2 equipas em {}".format(path))
    team_ids = tuple(team.get("id") for team in teams)
    team_names = tuple(team.findtext("Name") for team in teams)
    players = list(root.iter("Player"))
    team_of = np.array([0 if player.get("teamId") == team_ids[0] else 1
                        for player in players], dtype=np.int8)
    return team_ids, team_names, team_of, len(players)


def parse_raw(path, slots):
    players, ball = [], []
    with Path(path).open() as handle:
        for line in handle:
            _, groups, ball_group = line.rstrip().split(":")
            values = np.fromstring(groups.replace(";", ","), sep=",", dtype=np.float32)
            if values.size != slots * 3:
                raise ValueError("frame com {} valores em vez de {}".format(values.size, slots * 3))
            players.append(values.reshape(slots, 3))
            ball.append(np.fromstring(ball_group, sep=",", dtype=np.float32))
    return np.stack(players), np.stack(ball)


def load(xml_path, txt_path, cache=None):
    team_ids, team_names, team_of, slots = parse_meta(xml_path)
    cache = Path(cache) if cache else None
    if cache and cache.is_file():
        saved = np.load(cache)
        players, ball = saved["players"], saved["ball"]
        if players.shape[1] != slots:
            raise ValueError("cache com {} slots, meta tem {}".format(players.shape[1], slots))
    else:
        players, ball = parse_raw(txt_path, slots)
        if cache:
            cache.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(cache, players=players, ball=ball)
    return ATD(players=players, ball=ball, team_of=team_of,
               team_ids=team_ids, team_names=team_names)
