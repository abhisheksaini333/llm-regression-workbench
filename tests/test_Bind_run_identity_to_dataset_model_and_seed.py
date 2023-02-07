import unittest
from regression_workbench import config as m
class Contract(unittest.TestCase):
 def test_identity(self):
  self.assertTrue(hasattr(m,'run_identity'))
  c={'model':'m','prompt':'{input}'}
  self.assertEqual(m.run_identity('abc',c,1),m.run_identity('abc',dict(c),1))
  self.assertNotEqual(m.run_identity('abc',c,1),m.run_identity('abc',c,2))
