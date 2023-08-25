"""Server contracts."""

import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs,unquote
from pathlib import Path
from .store import Store
from .comparison import compare_runs
from .redaction import sanitize
from . import review

def create_server(db,port=8765,policy=None,static_dir=None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def send_json(self,status,value):
            body=json.dumps(sanitize(value),allow_nan=False).encode()
            self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
        def do_GET(self):
            try:
                parsed=urlparse(self.path)
                with Store(db) as store:
                    if parsed.path=='/api/runs': return self.send_json(200,store.list_runs())
                    if parsed.path.startswith('/api/runs/'):
                        identity=unquote(parsed.path[len('/api/runs/'):])
                        return self.send_json(200,dict(store.get_run(identity),results=store.results(identity)))
                self.send_json(404,{'error':'not found'})
            except KeyError:self.send_json(404,{'error':'run not found'})
            except ValueError as error:self.send_json(400,{'error':str(error)})
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)
