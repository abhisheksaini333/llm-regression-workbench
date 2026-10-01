import unittest
import tempfile
from pathlib import Path
from regression_workbench.evaluators import extraction, schema, tool

class MaintenanceLR04Tests(unittest.TestCase):

    def test_nested_boolean_number_values_never_compare_equal(self):
        self.assertTrue(extraction('{"a":[true]}', {'a': [1]})['score'] == 0)
        self.assertTrue(schema('{"a":true}', {'properties': {'a': {'enum': [1]}}})['score'] == 0)
        self.assertTrue(tool('{"tool":"x","arguments":{"a":{"b":true}}}', {'tool': 'x', 'arguments': {'a': {'b': 1}}})['score'] == 0)
        self.assertTrue(extraction('{"a":1.0}', {'a': 1})['score'] == 1)
