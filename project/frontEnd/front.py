from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2

app = Flask('FrontEnd')

BACKEND_IP = 'backEnd'
BACKEND_PORT = '5555'

def build_home_page(messages):
    ip = request.remote_addr
    response = requests.get('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/')
    data = None
    
    if response.status_code == 200:
        data = data = json.loads(response.content.decode('utf-8'))
    else:
        data = {'message':'erreur!'}
    content_basic = str(data)
    action_basic = 'action'

    return '''<html>
    <header></header>
    <body>
        <h1>TP3</h1>
        <h4>Réalisé par Gabriel bertrand et Keven Champagne</h4>
        <br>
        Message(s) basique:
		<ul>
			<li>''' + content_basic + '''</li>
		</ul>
        Message(s) d'action:
		<ul>
			<li>''' + action_basic + '''</li>
		</ul>
        <br>
        <h5>Login</h5>
        <form action="/login" method="POST">
            <label>Nom d'utilisateur: </label>
            <input type="text" name="username" required>
            <label>Mot de passe: </label>
            <input type="password" name="password" required>
            <button type="submit">Login</button>
        </form>
        <br>
        <h5>Recherche de compte</h5>
        <form action="/research" method="POST">
            <label>Terme de recherche: </label>
            <input type="text" name="searchTerm" required>
            <button type="submit">Rechercher</button>
        </form>
        <br>
        <h5>Voir son compte</h5>
        <a href="/viewAccount">Voir mon compte</a>
        <br>
        <h5>Transfert</h5>
        <form action="/transfert" method="POST">
            <label>Compte receveur: </label>
            <input type="text" name="account" required>
            <label>Montant: </label>
            <input type="text" name="amount" required>
            <button type="submit">Faire le transfer</button>
        </form>
        <br>
        <h5>Voir la FAQ</h5>
        <a href="/viewFaq">Voir la FAQ</a>
        <br>
        <h5>Ajouter un message à la FAQ</h5>
        <form action="/addFaqMsg" method="POST">
            <label>Message: </label>
            <input type="text" name="message" required>
            <button type="submit">Ajouter</button>
        </form>
        <br>
        <h5>Créer un compte</h5>
        <form action="/createAccount" method="POST">
            <label>Nom: </label>
            <input type="text" name="username" required>
            <label>Mot de passe: </label>
            <input type="password" name="password" required>
            <button type="submit">Créer le compte</button>
        </form>
    </body>
    </html>
    '''

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
    username = request.form['username']
    password = request.form['password']
    return build_home_page()

@app.route('/research', methods=['POST'])
def search():
    searchTerm = request.form['searchTerm']
    return build_home_page()

@app.route('/viewAccount', methods=['GET'])
def viewAccount():
    return build_home_page()

@app.route('/transfert', methods=['POST'])
def transfer():
    account = request.form['account']
    amount = request.form['amount']
    return build_home_page()

@app.route('/viewFaq', methods=['GET'])
def viewFaq():
    return build_home_page()

@app.route('/addFaqMsg', methods=['POST'])
def addFaqMsg():
    msg = request.form['message']
    return build_home_page()

@app.route('/createAccount', methods=['POST'])
def createAccount():
    account = request.form['username']
    amount = request.form['password']
    return build_home_page()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5556)