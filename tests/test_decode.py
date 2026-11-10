"""O Viterbi tem de preferir uma sequência coerente a um frame ruidoso."""
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_e1 import viterbi  # noqa: E402


class DecodeTests(unittest.TestCase):
    def test_noisy_frame_is_smoothed(self):
        logp = np.log(np.array([
            [0.90, 0.05, 0.05],
            [0.10, 0.45, 0.45],
            [0.90, 0.05, 0.05],
        ]))
        cost = np.full((3, 3), 5.0)
        np.fill_diagonal(cost, 0.0)
        path = viterbi(logp, cost)
        self.assertEqual(path.tolist(), [0, 0, 0])

    def test_strong_evidence_changes_state(self):
        logp = np.log(np.array([
            [0.90, 0.05, 0.05],
            [0.05, 0.90, 0.05],
            [0.90, 0.05, 0.05],
        ]))
        cost = np.full((3, 3), 0.5)
        np.fill_diagonal(cost, 0.0)
        path = viterbi(logp, cost)
        self.assertEqual(path.tolist(), [0, 1, 0])


if __name__ == "__main__":
    unittest.main()
