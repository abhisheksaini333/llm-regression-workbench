import unittest
from regression_workbench import server as m


class Contract(unittest.TestCase):
    def test_static_route(self):
        import tempfile, pathlib, threading, urllib.request, urllib.error
        from regression_workbench.store import Store

        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            (p / "index.html").write_text("<main>Workbench</main>")
            with Store(p / "r.db"):
                pass
            server = m.create_server(p / "r.db", port=0, static_dir=p)
            t = threading.Thread(
                target=lambda: server.serve_forever(poll_interval=0.01), daemon=True
            )
            t.start()
            try:
                base = "http://127.0.0.1:" + str(server.server_port)
                self.assertIn(b"Workbench", urllib.request.urlopen(base + "/").read())
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + "/%2e%2e/private")
                self.assertEqual(error.exception.code, 403)
            finally:
                server.shutdown()
                server.server_close()
                t.join()
