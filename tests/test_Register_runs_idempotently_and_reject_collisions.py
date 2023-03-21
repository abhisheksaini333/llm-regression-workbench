import unittest
from regression_workbench import store as m
class Contract(unittest.TestCase):
 def test_register(self):
  with m.Store(':memory:') as s:
   self.assertTrue(hasattr(s,'register'))
   s.register('r','d',{'model':'x'},0,2);s.register('r','d',{'model':'x'},0,2)
   self.assertEqual(s.connection.execute('select count(*) from runs').fetchone()[0],1)
   with self.assertRaises(ValueError): s.register('r','other',{},0,2)
