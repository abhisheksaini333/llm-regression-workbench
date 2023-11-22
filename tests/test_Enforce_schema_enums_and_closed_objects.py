import unittest
from regression_workbench import evaluators as m


class Contract(unittest.TestCase):
    def test_closed(self):
        e = {
            "additionalProperties": False,
            "properties": {"status": {"enum": ["ok", "no"]}},
        }
        self.assertEqual(m.schema('{"status":"maybe"}', e)["score"], 0)
        self.assertEqual(m.schema('{"status":"ok","x":1}', e)["score"], 0)
        self.assertEqual(m.schema('{"status":"ok"}', e)["score"], 1)
