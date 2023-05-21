import unittest
from regression_workbench import comparison as m
class Contract(unittest.TestCase):
 def test_critical_gate(self):
  self.assertTrue(hasattr(m,'gate'))
  a=[{'case_id':str(i),'task':'tool','slices':['critical'] if i==0 else [],'score':1 if i==0 else 0} for i in range(4)]
  b=[dict(r,score=0 if i==0 else 1) for i,r in enumerate(a)]
  c=m.compare(a,b)
  self.assertGreater(c['overall']['delta'],0)
  g=m.gate(c,{'critical':{'minimum':0.8,'max_regression':0.05}})
  self.assertFalse(g['passed']);self.assertEqual(g['failures'][0]['slice'],'critical')
