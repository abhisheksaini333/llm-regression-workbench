import unittest
from regression_workbench import dataset as m
class Contract(unittest.TestCase):
 def test_envelope(self):
  self.assertTrue(hasattr(m,'validate'))
  self.assertEqual(m.validate({'version':1,'name':'demo','cases':[]})['name'],'demo')
  for d in ({'version':2,'name':'d','cases':[]},{'version':1,'name':'','cases':[]},{'version':1,'name':'d','cases':'bad'}):
   with self.assertRaises(ValueError): m.validate(d)
