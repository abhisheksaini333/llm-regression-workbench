import unittest
from regression_workbench import review as m
class Contract(unittest.TestCase):
 def test_calibration(self):
  self.assertTrue(hasattr(m,'calibrate'))
  pairs=[{'case_id':'a','delta':0.1},{'case_id':'b','delta':0.8}]
  labels=[{'case_id':'a','preference':'tie'},{'case_id':'b','preference':'candidate'}]
  c=m.calibrate(pairs,labels,[0,0.2,0.9])
  self.assertEqual(c['selected_threshold'],0.2);self.assertEqual(c['agreement'],1)
  with self.assertRaises(ValueError): m.calibrate(pairs,labels[:1])
