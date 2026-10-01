import unittest
import tempfile
from pathlib import Path
import sqlite3
from regression_workbench.store import Store

class MaintenanceLR11Tests(unittest.TestCase):

    def test_unknown_schema_is_not_relabelled(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp_path = Path(directory.name)
        path = tmp_path / 'future.db'
        with sqlite3.connect(path) as db:
            db.execute('PRAGMA user_version=2')
        with self.assertRaises(ValueError):
            Store(path)
        with sqlite3.connect(path) as db:
            self.assertTrue(db.execute('PRAGMA user_version').fetchone()[0] == 2)
            self.assertTrue(db.execute('SELECT count(*) FROM sqlite_master').fetchone()[0] == 0)
