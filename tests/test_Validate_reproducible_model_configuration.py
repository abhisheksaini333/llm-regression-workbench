import unittest
from regression_workbench import config as m


class Contract(unittest.TestCase):
    def test_config(self):
        self.assertTrue(hasattr(m, "validate"))
        c = {"model": "fixture", "prompt": "{input}", "parameters": {"temperature": 0}}
        self.assertEqual(m.validate(c)["model"], "fixture")
        with self.assertRaises(ValueError):
            m.validate(dict(c, parameters={"temperature": -1}))
        with self.assertRaises(ValueError):
            m.validate(dict(c, model=""))
