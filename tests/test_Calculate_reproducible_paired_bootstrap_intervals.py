import unittest
from regression_workbench import comparison as m
class Contract(unittest.TestCase):
 def test_bootstrap(self):
  self.assertTrue(hasattr(m,'bootstrap'))
  a=m.bootstrap([1,-1,0.5,0],seed=7,resamples=500)
  self.assertEqual(a,m.bootstrap([1,-1,0.5,0],seed=7,resamples=500))
  self.assertLessEqual(a['low'],a['mean']);self.assertGreaterEqual(a['high'],a['mean'])
  self.assertAlmostEqual(m.bootstrap([0.2]*3)['low'],0.2)
  with self.assertRaises(ValueError): m.bootstrap([])
