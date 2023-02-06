import unittest
from regression_workbench import config as m
class Contract(unittest.TestCase):
 def test_render(self):
  self.assertTrue(hasattr(m,'render'))
  self.assertEqual(m.render({'model':'m','prompt':'Answer: {input}'},'{secret}'), 'Answer: {secret}')
