import unittest
from regression_workbench import store as m
class Contract(unittest.TestCase):
 def test_guard(self):
  with m.Store(':memory:') as s:
   s.register('r','d',{},0,1);s.claim('r','new',10,now=100)
   self.assertTrue(hasattr(s,'save_owned_result'))
   with self.assertRaises(RuntimeError): s.save_owned_result('r','a',{},'old')
   s.save_owned_result('r','a',{'score':1},'new')
