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
    data = {'status' : False, 'action' : 'login', 'id' : ''}
    if(request.method == 'GET'):
        result = valid_login(request.args.get('email',''),
            request.args.get('password',''))
        if result[0]:
            data['status'] = True
            data['id'] = result[1]
        return json.dumps(data)

@app.route('/logout',methods=['DELETE'])
def logout():
    id = request.args.get('id','')
    data = {'status' : False, 'action' : 'logout', 'id' : id}
    if(id != ''):
        server.connect()
        check_logout = server.delete_connection(id)
        server.close()

        if(check_logout[0] == 'Ok'):
            print('id: %s has been logged out' % id)
            data['status'] = True
        else:
            print('Problem occurs: %s' % check_logout[1])
    else:
        print('No received id')
    return json.dumps(data)


def valid_login(email,password):
    server.connect()
    check_login = server.check_auth_enter(email,password,'') #  ip later
    server.close()
    
    if(check_login[0] == 'Ok'):
        print('id:',check_login[1])
        print('Password:',password)
        return (True,check_login[1])
    else:
        return (False,check_login[1])

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