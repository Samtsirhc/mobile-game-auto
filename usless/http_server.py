from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import string
import urllib.parse as urlp
from threading import Thread

data = {'result': 'this is a test'}
host = ('localhost', 8888)
 
class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        _command = self.get_command()
        self.wfile.write(json.dumps(data).encode())

    def get_command(self):
        return self.extract(self.requestline)

    def extract(self, context):
        _tmp = context
        _tmp = _tmp.replace('GET /', '')
        _tmp = _tmp.replace(' HTTP/1.1', '')
        return urlp.unquote(_tmp)

        
if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()



