import unittest
from regression_workbench.providers import TransformersProvider
class ModelContract(unittest.TestCase):
 def test_temperature_is_not_silently_ignored(self):
  provider=TransformersProvider.__new__(TransformersProvider)
  with self.assertRaisesRegex(ValueError,'temperature=0'):
   provider.generate('prompt',{'id':'case'},{'parameters':{'temperature':1}})
