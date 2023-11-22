import unittest
from regression_workbench import evaluators as m


class Contract(unittest.TestCase):
    def test_tool(self):
        self.assertTrue(hasattr(m, "tool"))
        self.assertEqual(
            m.tool('{"tool":"lookup","arguments":{}}', {"tool": "lookup"})["score"], 1
        )
        self.assertEqual(m.tool('{"tool":"delete"}', {"tool": "lookup"})["score"], 0)
