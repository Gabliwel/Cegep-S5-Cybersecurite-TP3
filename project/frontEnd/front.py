from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2

app = Flask('FrontEnd')

BACKEND_IP = 'backEnd'
BACKEND_PORT = '5555'

def build_home_page(messages):
    ip = request.remote_addr
    response = requests.get('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/', json={'ip':ip})
    data = None
    
    if response.status_code == 200:
        data = data = json.loads(response.content.decode('utf-8'))
    else:
        data = {'message':'erreur!'}
    my_content_basic = str(data)

    my_action_basic = str(messages)

    return render_template('home.html', content_basic=my_content_basic, action_basic=my_action_basic)

def build_response(response):
    if response.status_code == 200:
        obj = json.loads(response.content.decode('utf-8'))
        resp = make_response(build_home_page(obj))
        return resp
    else:
        msg = response.content.decode('utf-8')
        resp = make_response(build_home_page({'message':msg}))
        return resp

@app.route('/')
def hello():
	return build_home_page({})

@app.route('/login', methods=['POST'])
def login():
    ip = request.remote_addr
    data = {'ip':ip}
    response = requests.post('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/login', auth=(request.form['username'], request.form['password']), json=data)
    resp = build_response(response)
    if response.status_code == 200:
        obj = json.loads(response.content.decode('utf-8'))
        print(obj, flush =True)
        resp.set_cookie('jwt',obj['token'], httponly=True)

        #Pour le xss
        if obj['message'].endswith("Gandalf"):
            resp.set_cookie('xss', 'FLAG-4444444444')
        else:
            resp.set_cookie('xss', expires=0)

    return resp

@app.route('/research', methods=['POST'])
def search():
    searchTerm = request.form['searchTerm']
    data = {'ip':request.remote_addr, 'searchTerm':searchTerm}
    response = requests.post('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/search', json=data)
    return build_response(response)

@app.route('/viewAccount', methods=['GET'])
def viewAccount():
    data = {'ip':request.remote_addr}
    token = request.cookies.get('jwt')
    response = requests.get('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/user', json=data, headers={'x-access-token' : token})
    return build_response(response)

@app.route('/transfert', methods=['POST'])
def transfer():
    account = request.form['account']
    amount = request.form['amount']
    data = {'ip':request.remote_addr, 'account':account, 'amount':amount}
    token = request.cookies.get('jwt')
    response = requests.post('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/transfert', json=data, headers={'x-access-token' : token})
    return build_response(response)

@app.route('/viewFaq', methods=['GET'])
def viewFaq():
    data = {'ip':request.remote_addr}
    token = request.cookies.get('jwt')
    response = requests.get('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/faq', json=data, headers={'x-access-token' : token})
    return build_response(response)

@app.route('/addFaqMsg', methods=['POST'])
def addFaqMsg():
    msg = request.form['message']
    data = {'message':msg, 'ip':request.remote_addr}
    token = request.cookies.get('jwt')
    response = requests.post('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/faq', json=data, headers={'x-access-token' : token})
    return build_response(response)

@app.route('/createAccount', methods=['POST'])
def createAccount():
    account = request.form['username']
    password = request.form['password']
    data = {'name':account, 'password':password, 'ip':request.remote_addr}
    token = request.cookies.get('jwt')
    response = requests.post('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/user', json=data, headers={'x-access-token' : token})
    return build_response(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5556)