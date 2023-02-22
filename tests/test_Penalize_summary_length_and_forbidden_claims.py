import unittest
from regression_workbench import evaluators as m
class Contract(unittest.TestCase):
 def test_constraints(self):
  self.assertEqual(m.summary('service recovered guaranteed',{'keywords':['service'],'forbidden':['guaranteed']})['score'],0)
  self.assertEqual(m.summary('one two three',{'keywords':['one'],'max_words':2})['score'],0)
