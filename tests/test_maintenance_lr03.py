import unittest
import tempfile
from pathlib import Path
from regression_workbench.evaluators import parse_object, extraction, tool

class MaintenanceLR03Tests(unittest.TestCase):

    def test_duplicate_json_fields_are_invalid(self):
        self.assertTrue(parse_object('{"a":0,"a":1}') is None)
        self.assertTrue(parse_object('{"a":{"b":0,"b":1}}') is None)
        self.assertTrue(extraction('{"a":0,"a":1}', {'a': 1})['score'] == 0)
        self.assertTrue(parse_object('{"a":1}') == {'a': 1})
