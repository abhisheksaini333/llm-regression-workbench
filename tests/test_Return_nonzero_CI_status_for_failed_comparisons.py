import unittest
from regression_workbench import cli as m


class Contract(unittest.TestCase):
    def test_compare_exit(self):
        import tempfile, pathlib, contextlib, io
        from regression_workbench.store import Store

        with tempfile.TemporaryDirectory() as d:
            db = str(pathlib.Path(d) / "r.db")
            with Store(db) as s:
                for rid, score in [("a", 1), ("b", 0)]:
                    s.register(rid, "d", {}, 0, 1)
                    s.claim(rid, "o")
                    s.save_result(
                        rid, "x", {"task": "tool", "score": score, "status": "ok"}
                    )
                    s.finish(rid, "o", "complete")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.main(["compare", "a", "b", "--db", db]), 1)
