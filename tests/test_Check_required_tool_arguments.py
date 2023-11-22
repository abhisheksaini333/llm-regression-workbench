import unittest
from regression_workbench import evaluators as m


class Contract(unittest.TestCase):
    def test_arguments(self):
        e = {"tool": "lookup", "arguments": {"id": "42"}}
        self.assertEqual(
            m.tool('{"tool":"lookup","arguments":{"id":"43"}}', e)["score"], 0
        )
        self.assertEqual(
            m.tool('{"tool":"lookup","arguments":{"id":"42"}}', e)["score"], 1
        )
