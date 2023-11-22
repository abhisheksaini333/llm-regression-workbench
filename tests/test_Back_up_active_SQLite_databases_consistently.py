import unittest
from regression_workbench import store as m


class Contract(unittest.TestCase):
    def test_backup(self):
        import tempfile, pathlib

        with tempfile.TemporaryDirectory() as d:
            with m.Store(pathlib.Path(d) / "source.db") as s:
                s.register("r", "d", {}, 0, 1)
                s.save_result("r", "a", {"score": 1})
                self.assertTrue(hasattr(s, "backup"))
                s.backup(pathlib.Path(d) / "backup.db")
            with m.Store(pathlib.Path(d) / "backup.db") as s:
                self.assertEqual(s.results("r")[0]["score"], 1)
