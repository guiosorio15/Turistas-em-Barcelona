"""Verificações de fronteira: assets, contrato CSV e encaminhamento de paths."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from turistas import cli


class PipelineTests(unittest.TestCase):
    def test_missing_data_fails_without_generating_submission(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            with contextlib.redirect_stderr(io.StringIO()):
                result = cli.main(["reproduce", "--data-dir", temporary,
                                   "--output-dir", str(output)])
            self.assertEqual(result, 1)
            self.assertFalse(output.exists())
            self.assertEqual(len(cli.missing_assets(root, True)), 2)

    def test_explicit_data_dir_takes_precedence(self):
        with patch.dict("os.environ", {"MTAH_DATA_DIR": "/wrong/location"}):
            self.assertEqual(cli.data_root("."), Path.cwd())

    def test_official_validator_accepts_baseline_rejects_bad_frame_count(self):
        baseline = cli.VENDOR / "evaluation/results/baseline_smooth50.csv"
        cli.run_official("evaluation/validate_submission.py", baseline)
        with tempfile.TemporaryDirectory() as temporary:
            invalid = Path(temporary) / "invalid.csv"
            invalid.write_text("frame,label\n0,H\n")
            result = subprocess.run([sys.executable, str(cli.VENDOR / "evaluation/validate_submission.py"),
                                     str(invalid)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

    def test_config_rejects_output_path_escape(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = Path(temporary) / "bad.toml"
            config.write_text('[baseline]\nwindow=50\nsubmission_name="../outside.csv"\n')
            with self.assertRaises(ValueError):
                cli.load_config(config)

    def test_evaluate_passes_absolute_paths_and_public_gt(self):
        with patch.object(cli, "run_official") as run:
            self.assertEqual(cli.main(["evaluate", "--results", "folder with spaces"]), 0)
            args = run.call_args.args
            self.assertEqual(args[1:3], ("--gt", "public"))
            self.assertIn(Path("folder with spaces").resolve(), args)

    def test_synthetic_tracking_reproduces_identical_csv_and_manifest_hashes(self):
        # Fixture artificial: não contém etiquetas nem posições do jogo fornecido.
        with tempfile.TemporaryDirectory(prefix="turistas test ") as temporary:
            base = Path(temporary)
            tactical = base / "data with spaces" / "tactical"
            tactical.mkdir(parents=True)
            (tactical / "BAR-ATH_tactical_atd.xml").write_text(
                '<Root><Team id="h"><Name>Home synthetic</Name></Team>'
                '<Team id="a"><Name>Away synthetic</Name></Team>'
                '<Player teamId="h"/><Player teamId="a"/></Root>')
            (tactical / "BAR-ATH_tactical_atd.txt").write_text(
                "1:0.1,0.1,0;0.9,0.9,0:0.1,0.1,0\n"
                "101:0.1,0.1,0;0.9,0.9,0:0.9,0.9,0\n")
            hashes = []
            for number in range(2):
                output = base / f"output {number}"
                self.assertEqual(cli.main(["reproduce", "--data-dir", str(tactical.parent),
                                           "--output-dir", str(output)]), 0)
                submission = output / "Turistas_de_la_Nave.csv"
                manifest = json.loads(submission.with_suffix(".manifest.json").read_text())
                self.assertEqual(manifest["submission_sha256"], cli.sha256(submission))
                hashes.append(manifest["submission_sha256"])
                with submission.open() as handle:
                    self.assertEqual(sum(1 for _ in handle), 199320)
            self.assertEqual(hashes[0], hashes[1])


if __name__ == "__main__":
    unittest.main()
