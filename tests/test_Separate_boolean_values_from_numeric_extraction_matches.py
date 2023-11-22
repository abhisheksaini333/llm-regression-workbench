import unittest
from regression_workbench import evaluators as m


class Contract(unittest.TestCase):
    def test_bool(self):
        self.assertEqual(m.extraction('{"count":true}', {"count": 1})["score"], 0)
        self.assertEqual(m.extraction('{"count":1.0}', {"count": 1})["score"], 1)
