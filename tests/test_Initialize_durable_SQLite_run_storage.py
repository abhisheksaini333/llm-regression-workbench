import unittest
from regression_workbench import store as m


class Contract(unittest.TestCase):
    def test_schema(self):
        import tempfile, pathlib

        self.assertTrue(hasattr(m, "Store"))
        with tempfile.TemporaryDirectory() as d:
            s = m.Store(pathlib.Path(d) / "runs.db")
            self.assertEqual(
                s.connection.execute("pragma user_version").fetchone()[0], 1
            )
            self.assertEqual(
                s.connection.execute("pragma journal_mode").fetchone()[0], "wal"
            )
            s.close()
