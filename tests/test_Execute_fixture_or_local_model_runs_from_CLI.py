import unittest
from regression_workbench import cli as m


class Contract(unittest.TestCase):
    def test_run_arguments(self):
        p = m.parser()
        a = p.parse_args(
            ["run", "data.json", "--config", "model.json", "--outputs", "outputs.json"]
        )
        self.assertEqual(a.outputs, "outputs.json")
        self.assertEqual(a.max_attempts, 3)
