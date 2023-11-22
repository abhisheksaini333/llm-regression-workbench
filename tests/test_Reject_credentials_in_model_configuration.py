import unittest
from regression_workbench import config as m


class Contract(unittest.TestCase):
    def test_secret(self):
        with self.assertRaises(ValueError):
            m.validate(
                {"model": "m", "prompt": "{input}", "parameters": {"api_key": "secret"}}
            )
