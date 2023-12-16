import unittest,tempfile,pathlib,io,hashlib
from regression_workbench import artifacts
class ArtifactContract(unittest.TestCase):
 def test_verified_download_and_reuse(self):
  self.assertTrue(hasattr(artifacts,'download'))
  content=b'model';row={'file':'weights.bin','url':'https://example.invalid/w','sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}
  calls=[]
  def fetch(url,timeout):calls.append(url);return io.BytesIO(content)
  with tempfile.TemporaryDirectory() as d:
   artifacts.download([row],d,fetch);artifacts.download([row],d,fetch)
   self.assertEqual(len(calls),1)
   self.assertEqual((pathlib.Path(d)/'weights.bin').read_bytes(),content)
   with self.assertRaises(ValueError):artifacts.download([dict(row,file='../escape')],d,fetch)
 def test_corruption_never_becomes_a_cached_model(self):
  self.assertTrue(hasattr(artifacts,'download'))
  row={'file':'weights.bin','url':'https://example.invalid/w','sha256':'wrong','bytes':3}
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):artifacts.download([row],d,lambda *a,**k:io.BytesIO(b'bad'))
   self.assertFalse((pathlib.Path(d)/'weights.bin').exists())
