import unittest

from tornado.httputil import HTTPConnection, HTTPHeaders, HTTPServerRequest
from airbrake.airbrake import _traceback_line


class Context(object):
    remote_ip = "127.0.0.1"


def http_request(uri, method="GET", body=None, headers=None):
    _headers = headers or dict()
    conn = HTTPConnection()
    conn.context = Context()

    return HTTPServerRequest(method=method,
                             uri=uri,
                             body=body,
                             host="localhost",
                             connection=conn,
                             headers=HTTPHeaders(**_headers))


class UnitTest(unittest.TestCase):

    def test_traceback_line(self):

        # Airbrake payloads contain tracebacks as arrays of <line> elements.
        _filename = "foo.py"
        _line = "1"
        _method = "__init__()"

        el = _traceback_line(_filename, _line, _method)

        self.assertEqual(el.attrib.get("number"), _line)
        self.assertEqual(el.attrib.get("file"), _filename)
        self.assertEqual(el.attrib.get("method"), _method)
        self.assertEqual(el.tag, "line")
