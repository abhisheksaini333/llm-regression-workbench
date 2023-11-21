"""Kill a real worker after persisted progress, then recover its SQLite lease."""
import json
import pathlib
import subprocess
import tempfile
import time
import unittest
from regression_workbench.providers import FixtureProvider
from regression_workbench.store import Store
from regression_workbench.runner import run

class ProcessRecovery(unittest.TestCase):
    def test_killed_worker_resumes_without_duplicate_results(self):
        data={'version':1,'name':'restart-fixture','cases':[{'id':i,'task':'tool','input':'lookup','expected':{'tool':'lookup'}} for i in ('a','b')]}
        config={'model':'fixture','prompt':'{input}'}
        outputs={i:'{"tool":"lookup"}' for i in ('a','b')}
        with tempfile.TemporaryDirectory() as directory:
            db=str(pathlib.Path(directory)/'runs.db')
            script='''import json,sys,time
from regression_workbench.providers import FixtureProvider
from regression_workbench.store import Store
from regression_workbench.runner import run
class Slow(FixtureProvider):
 def generate(self,prompt,case,config):
  if case['id']=='b':time.sleep(30)
  return super().generate(prompt,case,config)
data,config,outputs=json.loads(sys.argv[2])
with Store(sys.argv[1]) as store:run(data,config,Slow(outputs),store,lease_seconds=.3)
'''
            child=subprocess.Popen(['python3','-c',script,db,json.dumps([data,config,outputs])])
            try:
                deadline=time.monotonic()+10
                while time.monotonic()<deadline:
                    if pathlib.Path(db).exists():
                        with Store(db) as store:
                            runs=store.list_runs()
                            if runs and runs[0]['completed']==1:break
                    time.sleep(.02)
                else:self.fail('worker did not persist first result')
                child.kill();child.wait(timeout=5)
                time.sleep(.35)
                with Store(db) as store:
                    identity=run(data,config,FixtureProvider(outputs),store)
                    self.assertEqual(store.get_run(identity)['status'],'complete')
                    self.assertEqual([r['case_id'] for r in store.results(identity)],['a','b'])
                    self.assertEqual(store.connection.execute('SELECT count(*) FROM results').fetchone()[0],2)
            finally:
                if child.poll() is None:child.kill();child.wait(timeout=5)
