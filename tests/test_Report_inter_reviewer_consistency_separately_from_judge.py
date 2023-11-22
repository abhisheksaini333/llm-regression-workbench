import unittest
from regression_workbench import review as m


class Contract(unittest.TestCase):
    def test_reviewers(self):
        self.assertTrue(hasattr(m, "reviewer_consistency"))
        labels = [
            {"case_id": "a", "reviewer": "u", "preference": "tie"},
            {"case_id": "a", "reviewer": "v", "preference": "tie"},
            {"case_id": "b", "reviewer": "u", "preference": "baseline"},
            {"case_id": "b", "reviewer": "v", "preference": "candidate"},
        ]
        self.assertEqual(
            m.reviewer_consistency(labels), {"paired_cases": 2, "agreement": 0.5}
        )
