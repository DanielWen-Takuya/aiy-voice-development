from flask import Flask
from flask import request
import json

from postgre_server import PostgreServer

app = Flask(__name__)

server = PostgreServer('qwertyuiop')

@app.route('/')
def check_server():
    data = {'status' : True, 'action' : 'check'}
    return json.dumps(data)

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    data = {'status' : False, 'action' : 'login', 'email' : ''}
    if request.method == 'GET':
        data['email'] = request.args.get('email','') #  need to get from database
        if valid_login(request.args.get('email',''),
            request.args.get('password','')):
            data['status'] = True
        return json.dumps(data)


def valid_login(email,password):
    server.connect()
    check_login = server.check_auth_enter(email,password,'') #  ip later
    server.close()
    
    if(check_login[0] == 'Ok'):
        print('id:',check_login[1])
        print('Password:',password)
        return True
    else:
        return False

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