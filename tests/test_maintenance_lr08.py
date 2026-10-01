import unittest
import tempfile
from pathlib import Path
from regression_workbench.review import calibrate

class MaintenanceLR08Tests(unittest.TestCase):

    def test_orphan_reviews_do_not_qualify_calibration(self):
        pairs = [{'case_id': 'a', 'delta': 0.1}]
        labels = [{'case_id': 'x', 'preference': 'tie'}, {'case_id': 'y', 'preference': 'tie'}]
        with self.assertRaises(ValueError):
            calibrate(pairs, labels)

    def test_duplicate_reviewers_do_not_multiply_evidence(self):
        pairs = [{'case_id': 'a', 'delta': 0.1}]
        label = {'case_id': 'a', 'reviewer': 'u', 'preference': 'tie'}
        with self.assertRaises(ValueError):
            calibrate(pairs, [label, label])
