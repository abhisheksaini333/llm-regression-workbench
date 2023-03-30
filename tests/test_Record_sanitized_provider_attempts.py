import unittest
from regression_workbench import store as m
class Contract(unittest.TestCase):
 def test_attempts(self):
  with m.Store(':memory:') as s:
   s.register('r','d',{},0,1)
   self.assertTrue(hasattr(s,'record_attempt'))
   s.record_attempt('r','a',{'error':'Bearer abc','attempt':1})
   self.assertNotIn('abc',str(s.attempts('r')))
