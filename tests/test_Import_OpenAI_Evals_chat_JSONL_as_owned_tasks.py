import unittest
from regression_workbench import adapters as m


class Contract(unittest.TestCase):
    def test_adapter(self):
        import tempfile, pathlib, json

        self.assertTrue(hasattr(m, "import_evals"))
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "eval.jsonl"
            p.write_text(
                json.dumps(
                    {
                        "input": [{"role": "user", "content": "Find name"}],
                        "ideal": "Ada",
                    }
                )
                + "\n"
            )
            data = m.import_evals(p)
            self.assertEqual(data["cases"][0]["input"], "user: Find name")
            self.assertEqual(data["cases"][0]["expected"]["keywords"], ["Ada"])
