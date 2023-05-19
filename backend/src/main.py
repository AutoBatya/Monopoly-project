from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import json


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            json_data = {'token': 'test_test'}
            json_data['test'] = 'test_test_test'
            self.wfile.write(json.dumps(json_data).encode('utf-8'))
        else:
            self.send_error(404)


def run(handler_class=BaseHTTPRequestHandler):
    port = 8000
    server_address = ('', port)
    server = HTTPServer(server_address, handler_class)
    print(f'Server started at port {port}. Press CTRL+C to close the server.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server Closed")


if __name__ == '__main__':
    run(HTTPRequestHandler)
