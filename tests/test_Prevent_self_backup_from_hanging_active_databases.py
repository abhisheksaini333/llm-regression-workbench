import unittest
from regression_workbench import store as m


class Contract(unittest.TestCase):
    def test_self_backup(self):
        import pathlib, tempfile

        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "r.db"
            with m.Store(p) as s:
                with self.assertRaises(ValueError):
                    s.backup(p)
