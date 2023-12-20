import unittest
from regression_workbench.comparison import validate_policy


class PolicyContract(unittest.TestCase):
    def test_misspelling_cannot_silently_disable_a_gate(self):
        for policy in (
            {"critcal": {}},
            {"critical": {"important": {"minumum": 0.9}}},
            {"budgets": {"max_error": 0}},
        ):
            with self.assertRaises(ValueError):
                validate_policy(policy)
