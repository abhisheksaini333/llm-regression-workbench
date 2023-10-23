import unittest
from regression_workbench import server as m
class Contract(unittest.TestCase):
 def test_host_and_headers(self):
  from tests.http_support import running
  import urllib.request,urllib.error
  with running() as (base,db):
   req=urllib.request.Request(base+'/api/runs',headers={'Host':'attacker.invalid'})
   with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(req)
   self.assertEqual(e.exception.code,403)
   response=urllib.request.urlopen(base+'/api/runs')
   self.assertEqual(response.headers['X-Content-Type-Options'],'nosniff')
