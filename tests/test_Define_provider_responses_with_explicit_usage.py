import unittest
from regression_workbench import providers as m
class Contract(unittest.TestCase):
 def test_response(self):
  self.assertTrue(hasattr(m,'Response'))
  r=m.Response('hello',3,2,'tokens',{'provider':'fixture'})
  self.assertEqual(r.output,'hello')
  with self.assertRaises(ValueError): m.Response('x',-1,0)
