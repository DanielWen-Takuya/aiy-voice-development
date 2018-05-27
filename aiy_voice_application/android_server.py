from http.server import BaseHTTPRequestHandler, HTTPServer

class AndroidServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.wfile.write(bytes("abcdefg","utf-8"))

def run(server_class=HTTPServer, handler_class=AndroidServer, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()