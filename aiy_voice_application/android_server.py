from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def check_server():
    return 'Server is active!'

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'GET':
        if valid_login(request.args.get('username',''),
            request.args.get('password','')):
            return 'OK'

def valid_login(username,password):
    print('Username:',username)
    print('Password:',password)
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

'''from http.server import BaseHTTPRequestHandler, HTTPServer

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
'''