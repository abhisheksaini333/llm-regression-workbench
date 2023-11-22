import unittest, tempfile, pathlib, subprocess, json
from regression_workbench.store import Store


class DemoContract(unittest.TestCase):
    def test_demo_repeats_without_duplicate_cases(self):
        self.assertTrue(pathlib.Path("scripts/demo.py").is_file())
        with tempfile.TemporaryDirectory() as d:
            db = str(pathlib.Path(d) / "r.db")
            for _ in range(2):
                result = subprocess.run(
                    ["python3", "scripts/demo.py", "--db", db],
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertFalse(output["gate"]["passed"])
            with Store(db) as s:
                self.assertEqual(
                    s.connection.execute("SELECT count(*) FROM results").fetchone()[0],
                    48,
                )
