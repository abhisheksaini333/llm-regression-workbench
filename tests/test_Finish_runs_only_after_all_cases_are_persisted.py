import unittest
from regression_workbench import store as m
class Contract(unittest.TestCase):
 def test_finish(self):
  with m.Store(':memory:') as s:
   s.register('r','d',{},0,1);s.claim('r','one')
   self.assertTrue(hasattr(s,'finish'))
   with self.assertRaises(ValueError): s.finish('r','one','complete')
   s.save_result('r','a',{});s.finish('r','one','complete')
   self.assertEqual(s.get_run('r')['status'],'complete')
   self.assertIsNone(s.get_run('r')['owner'])
