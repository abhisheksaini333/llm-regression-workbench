import unittest
from regression_workbench import dataset as m
class Contract(unittest.TestCase):
 def test_order_and_unicode(self):
  self.assertTrue(hasattr(m,'canonical'))
  self.assertEqual(m.canonical({'b':2,'a':'é'}),m.canonical({'a':'é','b':2}))
  with self.assertRaises(ValueError): m.canonical({'x':float('nan')})
