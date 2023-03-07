import unittest
from regression_workbench import evaluators as m
class Contract(unittest.TestCase):
 def test_aggregate(self):
  self.assertTrue(hasattr(m,'aggregate'))
  a=m.aggregate([{'task':'tool','score':1},{'task':'tool','score':0},{'task':'summary','score':0.5}])
  self.assertEqual(a['tool'],{'count':2,'mean':0.5})
  self.assertEqual(m.aggregate([]),{})
