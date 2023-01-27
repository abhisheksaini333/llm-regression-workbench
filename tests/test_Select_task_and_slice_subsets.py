import unittest
from regression_workbench import dataset as m
class Contract(unittest.TestCase):
 def test_select(self):
  self.assertTrue(hasattr(m,'select'))
  a={'id':'a','task':'tool','input':'hi','expected':{},'slices':['critical']}
  b=dict(a,id='b',task='summary',slices=[])
  d={'version':1,'name':'x','cases':[a,b]}
  self.assertEqual([c['id'] for c in m.select(d,slice_name='critical')['cases']],['a'])
  self.assertEqual(len(m.select(d,task='summary')['cases']),1)
