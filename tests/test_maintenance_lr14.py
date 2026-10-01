import unittest
import tempfile
from pathlib import Path
import hashlib, io
from regression_workbench.artifacts import download

class MaintenanceLR14Tests(unittest.TestCase):

    def test_cached_artifact_cannot_be_a_symlink(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp_path = Path(directory.name)
        outside = tmp_path / 'outside'
        outside.write_bytes(b'model')
        cache = tmp_path / 'cache'
        cache.mkdir()
        (cache / 'model.bin').symlink_to(outside)
        row = {'file': 'model.bin', 'url': 'https://example.org/model', 'bytes': 5, 'sha256': hashlib.sha256(b'model').hexdigest()}
        with self.assertRaises(ValueError):
            download([row], cache, lambda *a, **k: io.BytesIO(b'model'))
        self.assertTrue(outside.read_bytes() == b'model')

    def test_racing_artifact_is_not_overwritten(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        tmp_path = Path(directory.name)
        row = {'file': 'model.bin', 'url': 'https://example.org/model', 'bytes': 5, 'sha256': hashlib.sha256(b'model').hexdigest()}

        def fetch(*a, **k):
            (tmp_path / 'model.bin').write_bytes(b'racing')
            return io.BytesIO(b'model')
        with self.assertRaises((ValueError, FileExistsError)):
            download([row], tmp_path, fetch)
        self.assertTrue((tmp_path / 'model.bin').read_bytes() == b'racing')
