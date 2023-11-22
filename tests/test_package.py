import unittest
import regression_workbench as package


class PackageTest(unittest.TestCase):
    def test_version(self):
        self.assertEqual(package.__version__, "0.1.0")
