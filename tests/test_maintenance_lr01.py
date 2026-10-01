import unittest
import tempfile
from pathlib import Path
from regression_workbench.dataset import validate

class MaintenanceLR01Tests(unittest.TestCase):

    def test_strict_dataset_version(self):
        for version in [True, 1.0]:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    validate({'version': version, 'name': 'd', 'cases': []})

    def test_nonfinite_dataset_content(self):
        with self.assertRaises(ValueError):
            validate({'version': 1, 'name': 'd', 'cases': [], 'metadata': {'score': float('nan')}})
