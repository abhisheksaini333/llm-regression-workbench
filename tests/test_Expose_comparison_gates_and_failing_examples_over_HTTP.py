import unittest
from regression_workbench import server as m
class Contract(unittest.TestCase):
 def test_comparison_route(self):
  import inspect
  self.assertIn("'/api/compare'",inspect.getsource(m.create_server))
