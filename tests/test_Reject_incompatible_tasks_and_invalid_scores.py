import unittest
from regression_workbench import comparison as m
class Contract(unittest.TestCase):
 def test_compatibility(self):
  a=[{'case_id':'a','score':1,'task':'tool','slices':['critical']}]
  for b in ([dict(a[0],task='summary')],[dict(a[0],score=float('nan'))],[dict(a[0],slices=[])]):
   with self.assertRaises(ValueError): m.pair(a,b)
