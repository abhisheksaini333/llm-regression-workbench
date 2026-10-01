import unittest
import tempfile
from pathlib import Path
from regression_workbench.store import Store

class MaintenanceLR12Tests(unittest.TestCase):

    def test_backup_refuses_existing_destinations(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp_path = Path(directory.name)
        target = tmp_path / 'backup.db'
        target.write_bytes(b'preserve')
        with Store(tmp_path / 'live.db') as store:
            with self.assertRaises(ValueError):
                store.backup(target)
        self.assertTrue(target.read_bytes() == b'preserve')

    def test_backup_is_private(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp_path = Path(directory.name)
        target = tmp_path / 'backup.db'
        with Store(tmp_path / 'live.db') as store:
            store.backup(target)
        self.assertTrue(target.stat().st_mode & 511 == 384)
