import config
import json
import os
import sys
import threading
import controllers

from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class HTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, req, client_addr, server):
        super().__init__(req, client_addr, server, directory=config.www_root())

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/api':
            self._set_headers()
            query_string = parse_qs(parsed_path.query)

            if "controller" not in query_string:
                return self.error("missing controller")

            controller = query_string['controller'][0]

            if not f'controllers.{controller}' in sys.modules:
                return self.error(f"unknown controller {controller}")

            module = sys.modules[f'controllers.{controller}']

            if "method" not in query_string:
                return self.error("missing controller's method name")

            method = query_string['method'][0]

            if not hasattr(module, method):
                return self.error(f"unknown method {method} in controller {controller}")

            callback = getattr(module, method)

            payload = callback(query_string)

            msg = json.dumps({
                "status": "ok",
                "payload": payload
            }).encode('UTF-8')
            self.wfile.write(msg)
        else:
            super().do_GET()
        return

    def do_POST(self):
        self._set_header()
        msg = json.dumps({"message": "Hello, POST"}).encode('UTF-8')
        print(f"msg : {msg}")
        self.wfile.write(msg)
        return

    def error(self, message):
        msg = json.dumps({
            "status": "error",
            "message": message,
        }).encode('UTF-8')
        self.wfile.write(msg)
        return None


def start_web_server():
    server = HTTPServer(('localhost', 8765), HTTPRequestHandler)
    print('Starting server at http://localhost:8765')
    t = threading.Thread(target=lambda s: s.serve_forever(), args=([server]))
    t.daemon = True
    t.start()
    return t
