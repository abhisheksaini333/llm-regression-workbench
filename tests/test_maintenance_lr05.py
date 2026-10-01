import unittest
import tempfile
from pathlib import Path
from regression_workbench.comparison import pair

class MaintenanceLR05Tests(unittest.TestCase):

    def test_scores_validated_before_delta(self):
        for bad in [True, '0.5', None]:
            with self.subTest(bad=bad):
                a = {'case_id': 'x', 'score': 0.5, 'task': 'summary'}
                with self.assertRaises(ValueError):
                    pair([a], [dict(a, score=bad)])
