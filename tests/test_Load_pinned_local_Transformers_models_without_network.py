import unittest
from regression_workbench import providers as m
class Contract(unittest.TestCase):
 def test_missing_local_model(self):
  self.assertTrue(hasattr(m,'TransformersProvider'))
  with self.assertRaises(ValueError): m.TransformersProvider('/missing/model','revision')
