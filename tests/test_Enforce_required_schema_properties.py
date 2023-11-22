import unittest
from regression_workbench import evaluators as m


class Contract(unittest.TestCase):
    def test_schema(self):
        self.assertTrue(hasattr(m, "schema"))
        expected = {"required": ["name"]}
        self.assertEqual(m.schema("{}", expected)["score"], 0)
        self.assertEqual(m.schema('{"name":"Ada"}', expected)["score"], 1)
