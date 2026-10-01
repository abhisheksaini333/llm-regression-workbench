import unittest
import tempfile
from pathlib import Path
from regression_workbench.comparison import operational

class MaintenanceLR07Tests(unittest.TestCase):

    def test_operational_measurements_reject_corruption(self):
        for field, bad in [('input_tokens', -1), ('output_tokens', True), ('output_tokens', 1.5), ('latency_ms', True), ('latency_ms', '2'), ('usage_kind', 'bogus')]:
            with self.subTest(field=field, bad=bad):
                row = {'latency_ms': 1, 'input_tokens': 2, 'output_tokens': 3, 'usage_kind': 'tokens'}
                row[field] = bad
                with self.assertRaises(ValueError):
                    operational([row])
