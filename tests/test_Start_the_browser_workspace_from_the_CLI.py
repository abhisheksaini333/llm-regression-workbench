import unittest
from regression_workbench import cli as m
class Contract(unittest.TestCase):
 def test_serve_options(self):
  args=m.parser().parse_args(['serve','--port','9876','--policy','policy.json'])
  self.assertEqual(args.port,9876);self.assertEqual(args.static,'frontend/dist')
