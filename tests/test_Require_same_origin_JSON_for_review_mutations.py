import unittest
from regression_workbench import server as m


class Contract(unittest.TestCase):
    def test_csrf(self):
        from tests.http_support import running, post
        import urllib.error

        with running() as (base, db):
            with self.assertRaises(urllib.error.HTTPError) as error:
                post(
                    base,
                    "/api/reviews",
                    {},
                    headers={
                        "Content-Type": "application/json",
                        "Origin": "https://attacker.invalid",
                    },
                )
            self.assertEqual(error.exception.code, 403)
