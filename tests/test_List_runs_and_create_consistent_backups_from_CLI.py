import unittest
from regression_workbench import cli as m


class Contract(unittest.TestCase):
    def test_backup_cli(self):
        import tempfile, pathlib, contextlib, io
        from regression_workbench.store import Store

        with tempfile.TemporaryDirectory() as d:
            db = str(pathlib.Path(d) / "r.db")
            backup = str(pathlib.Path(d) / "b.db")
            with Store(db) as s:
                s.register("r", "d", {}, 0, 0)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.main(["backup", backup, "--db", db]), 0)
            with Store(backup) as s:
                self.assertEqual(len(s.list_runs()), 1)
