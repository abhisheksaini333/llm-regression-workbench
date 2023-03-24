import unittest
from regression_workbench import store as m
class Contract(unittest.TestCase):
 def test_read(self):
  with m.Store(':memory:') as s:
   s.register('r','d',{},0,2);s.save_result('r','b',{'score':1});s.save_result('r','a',{'score':0})
   self.assertTrue(hasattr(s,'results'))
   self.assertEqual([r['case_id'] for r in s.results('r')],['a','b'])
   self.assertEqual(s.get_run('r')['completed'],2)
   self.assertEqual(s.list_runs()[0]['id'],'r')
   with self.assertRaises(KeyError): s.get_run('missing')
