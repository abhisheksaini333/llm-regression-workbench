import unittest
import tempfile
from pathlib import Path
from regression_workbench.config import validate

class MaintenanceLR02Tests(unittest.TestCase):

    def test_temperature_is_a_finite_number(self):
        for bad in [True, float('nan'), float('inf'), '0']:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate({'model': 'm', 'prompt': '{input}', 'parameters': {'temperature': bad}})
