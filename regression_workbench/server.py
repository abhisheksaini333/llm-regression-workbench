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
        def do_POST(self):
            allowed={'http://127.0.0.1:'+str(self.server.server_port),'http://localhost:'+str(self.server.server_port)}
            if self.headers.get('Origin') not in allowed: return self.send_json(403,{'error':'same-origin review required'})
            if self.headers.get_content_type()!='application/json': return self.send_json(415,{'error':'JSON content type required'})
            try:
                if urlparse(self.path).path!='/api/reviews': return self.send_json(404,{'error':'not found'})
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=16384: return self.send_json(413,{'error':'request body must be 1..16384 bytes'})
                data=json.loads(self.rfile.read(size))
                with Store(db) as store:
                    compare_runs(store,data['baseline'],data['candidate'],policy)
                    preference=review.unblind(data['case_id'],data['reviewer'],data['choice'])
                    label=review.save(store,data['baseline'],data['candidate'],data['case_id'],data['reviewer'],preference,data.get('note',''),data.get('revision'))
                    return self.send_json(200,{'saved':True,'revision':label['revision']})
            except (ValueError,KeyError,TypeError) as error:self.send_json(400,{'error':str(error)})
        def do_GET(self):
            try:
                parsed=urlparse(self.path)
                query=parse_qs(parsed.query)
                with Store(db) as store:
                    if parsed.path=='/api/review-analysis':
                        baseline=query.get('baseline',[''])[0];candidate=query.get('candidate',[''])[0]
                        compared=compare_runs(store,baseline,candidate,policy);labels=review.list_reviews(store,baseline,candidate)
                        analysis=review.agreement(compared['cases'],labels)
                        analysis['reviewers']=review.reviewer_consistency(labels)
                        if len([r for r in labels if r['preference']!='skip'])>=2: analysis['calibration']=review.calibrate(compared['cases'],labels)
                        return self.send_json(200,analysis)
                    if parsed.path=='/api/review':
                        baseline=query.get('baseline',[''])[0];candidate=query.get('candidate',[''])[0];reviewer=query.get('reviewer',[''])[0]
                        if not reviewer.strip(): raise ValueError('reviewer required')
                        comparison=compare_runs(store,baseline,candidate,policy)
                        labels=[r for r in review.list_reviews(store,baseline,candidate) if r['reviewer']==reviewer]
                        by_case={r['case_id']:r for r in labels}
                        return self.send_json(200,{'pairs':[dict(review.blind_pair(p,reviewer),revision=by_case.get(p['case_id'],{}).get('revision',0),reviewed=p['case_id'] in by_case) for p in comparison['cases']]})
                    if parsed.path=='/api/compare':
                        baseline=query.get('baseline',[''])[0];candidate=query.get('candidate',[''])[0]
                        return self.send_json(200,compare_runs(store,baseline,candidate,policy))
                    if parsed.path=='/api/runs': return self.send_json(200,store.list_runs())
                    if parsed.path.startswith('/api/runs/'):
                        identity=unquote(parsed.path[len('/api/runs/'):])
                        return self.send_json(200,dict(store.get_run(identity),results=store.results(identity)))
                if not parsed.path.startswith('/api/') and static_dir:
                    root=Path(static_dir).resolve()
                    requested=(root/unquote(parsed.path).lstrip('/')).resolve()
                    if not requested.is_relative_to(root): return self.send_json(403,{'error':'invalid path'})
                    target=requested if requested.is_file() else root/'index.html'
                    if target.is_file():
                        import mimetypes
                        body=target.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(str(target))[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
                self.send_json(404,{'error':'not found'})
            except KeyError:self.send_json(404,{'error':'run not found'})
            except ValueError as error:self.send_json(400,{'error':str(error)})
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)
