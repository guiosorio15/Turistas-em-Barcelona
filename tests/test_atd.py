"""Fronteiras do parser ATD: slots, equipas, bola em falta e cache."""
import tempfile
from pathlib import Path
import unittest

import numpy as np

from turistas import atd


class ATDTests(unittest.TestCase):
    def test_parse_and_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            xml = root / "meta.xml"
            raw = root / "raw.txt"
            cache = root / "cache.npz"
            xml.write_text(
                '<Root><Team id="h"><Name>Home</Name></Team>'
                '<Team id="a"><Name>Away</Name></Team>'
                '<Player id="1" teamId="h"/><Player id="2" teamId="a"/></Root>'
            )
            raw.write_text(
                "1:0.1,0.2,1.0;0.9,0.8,2.0:0.5,0.5,3.0\n"
                "2:NaN,NaN,NaN;0.9,0.8,2.0:NaN,NaN,NaN\n"
            )
            data = atd.load(xml, raw, cache=cache)
            self.assertEqual(data.players.shape, (2, 2, 3))
            self.assertEqual(data.ball.shape, (2, 3))
            self.assertEqual(data.team_of.tolist(), [0, 1])
            self.assertEqual(data.team_names, ("Home", "Away"))
            self.assertTrue(np.isnan(data.ball[1, 0]))
            cached = atd.load(xml, raw, cache=cache)
            np.testing.assert_array_equal(cached.players, data.players)
            np.testing.assert_array_equal(cached.ball, data.ball)


if __name__ == "__main__":
    unittest.main()
