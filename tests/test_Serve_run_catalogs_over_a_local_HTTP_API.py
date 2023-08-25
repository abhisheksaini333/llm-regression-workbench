import unittest
from regression_workbench import server as m
class Contract(unittest.TestCase):
 def test_catalog(self):
  import tempfile,pathlib,threading,urllib.request,json
  from regression_workbench.store import Store
  self.assertTrue(hasattr(m,'create_server'))
  with tempfile.TemporaryDirectory() as d:
   path=pathlib.Path(d)/'r.db'
   with Store(path) as s:s.register('r','d',{},0,1)
   server=m.create_server(path,port=0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
   try:
    value=json.load(urllib.request.urlopen('http://127.0.0.1:'+str(server.server_port)+'/api/runs'))
    self.assertEqual(value[0]['id'],'r')
   finally:server.shutdown();server.server_close();thread.join()
