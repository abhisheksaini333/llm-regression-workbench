import unittest
from regression_workbench import evaluators as m
class Contract(unittest.TestCase):
 def test_summary(self):
  self.assertTrue(hasattr(m,'summary'))
  self.assertEqual(m.summary('The service recovered.',{'keywords':['service','recovered']})['score'],1)
  self.assertEqual(m.summary('SERVICE still down',{'keywords':['service','recovered']})['score'],0.5)
