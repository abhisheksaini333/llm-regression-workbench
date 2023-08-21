import unittest,tempfile,pathlib,time
from regression_workbench.store import Store
class Contract(unittest.TestCase):
 def test_expired_owner_and_reclaim(self):
  with tempfile.TemporaryDirectory() as d:
   path=pathlib.Path(d)/'r.db'
   with Store(path) as one, Store(path) as two:
    one.register('r','d',{},0,1);one.claim('r','one',1,now=time.time()-2)
    with self.assertRaises(RuntimeError):one.save_owned_result('r','a',{},'one')
    with self.assertRaises(RuntimeError):one.finish('r','one','failed')
    two.claim('r','two')
    with self.assertRaises(RuntimeError):one.claim('r','one')
    two.save_owned_result('r','a',{'score':1},'two')
    two.finish('r','two','complete')
    self.assertEqual(len(one.results('r')),1)
