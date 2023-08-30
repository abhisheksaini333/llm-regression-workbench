import contextlib,tempfile,pathlib,threading,json,urllib.request
from regression_workbench.server import create_server
from regression_workbench.store import Store
@contextlib.contextmanager
def running(policy=None):
 with tempfile.TemporaryDirectory() as d:
  db=pathlib.Path(d)/'r.db'
  with Store(db) as s:
   for rid,score in [('a',1),('b',0)]:
    s.register(rid,'dataset',{},0,1);s.claim(rid,'owner');s.save_result(rid,'case',{'score':score,'task':'tool','slices':['critical'],'output':rid,'prompt':'Select tool','status':'ok'});s.finish(rid,'owner','complete')
  server=create_server(db,port=0,policy=policy);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:yield 'http://127.0.0.1:'+str(server.server_port),db
  finally:server.shutdown();server.server_close();thread.join()
def get(base,path):return json.load(urllib.request.urlopen(base+path))
def post(base,path,data,headers=None):
 request=urllib.request.Request(base+path,data=json.dumps(data).encode(),headers=headers or {'Content-Type':'application/json','Origin':base},method='POST')
 return json.load(urllib.request.urlopen(request))
