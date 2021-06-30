
import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.do_HEAD()
        logging.info("GET request received!")
        self.wfile.write("GET request received!".encode('utf-8'))

    def do_POST(self):
        # Get the size of data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # Get the data
        logging.info(f"POST request " + post_data.decode('utf-8'))
        self.do_HEAD()
        self.wfile.write("POST request received!".encode('utf-8'))

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
           <html><head><title>Title goes here.</title></head>
           <body><p>This is a test.</p>
           <p>You accessed path: {}</p>
           </body></html>
           '''.format(path)
        return bytes(content, 'UTF-8')


def run(server_class=HTTPServer, handler_class=Handler, port=8888):
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] : %(message)s',
                        datefmt='%H:%M:%S')
    server_address = ('localhost', port)
    server = server_class(server_address, handler_class)
    logging.info('Starting server...')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping server...')





if __name__ == '__main__':
    run()
