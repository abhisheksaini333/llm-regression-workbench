import unittest
from regression_workbench import evaluators as m
class Contract(unittest.TestCase):
 def test_nonfinite(self):
  self.assertIsNone(m.parse_object('{"value":NaN}'))
  self.assertIsNone(m.parse_object('{"value":Infinity}'))
  self.assertEqual(m.schema('{"x":NaN}',{})['score'],0)
