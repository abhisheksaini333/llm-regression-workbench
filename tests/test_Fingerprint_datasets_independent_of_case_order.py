import unittest
from regression_workbench import dataset as m
class Contract(unittest.TestCase):
 def test_fingerprint(self):
  self.assertTrue(hasattr(m,'fingerprint'))
  a={'id':'a','task':'tool','input':'hello','expected':{}}
  b=dict(a,id='b')
  d={'version':1,'name':'x','cases':[a,b]}
  self.assertEqual(m.fingerprint(d),m.fingerprint(dict(d,cases=[b,a])))
  self.assertNotEqual(m.fingerprint(d),m.fingerprint(dict(d,cases=[dict(a,input='changed'),b])))
