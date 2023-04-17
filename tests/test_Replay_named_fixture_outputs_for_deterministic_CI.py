import unittest
from regression_workbench import providers as m
class Contract(unittest.TestCase):
 def test_fixture(self):
  self.assertTrue(hasattr(m,'FixtureProvider'))
  p=m.FixtureProvider({'a':'answer'})
  self.assertEqual(p.generate('prompt',{'id':'a'},{}).output,'answer')
  with self.assertRaises(ValueError): p.generate('',{'id':'b'},{})
