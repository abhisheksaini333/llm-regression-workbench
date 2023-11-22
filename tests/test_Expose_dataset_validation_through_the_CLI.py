import unittest
from regression_workbench import cli as m


class Contract(unittest.TestCase):
    def test_validate_cli(self):
        import tempfile, pathlib, json, contextlib, io

        self.assertTrue(hasattr(m, "main"))
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "d.json"
            p.write_text(json.dumps({"version": 1, "name": "x", "cases": []}))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(m.main(["validate", str(p)]), 0)
            self.assertIn("fingerprint", json.loads(out.getvalue()))
