from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2

app = Flask('FrontEnd')

BACKEND_IP = 'backEnd'
BACKEND_PORT = '5555'

def build_home_page():
    ip = request.remote_addr
    response = requests.get('http://' + BACKEND_IP + ':' + BACKEND_PORT + '/test')
    data = None
    
    if response.status_code == 200:
        data = data = json.loads(response.content.decode('utf-8'))
    else:
        data = {'message':'erreur!'}
    content_basic = str(data)

    return '''<html>
    <header></header>
    <body>
        <p>Yes, un TP3 qui marche... je crois</p>
        <br>
        BASIC DATA:
		<ul>
			<li>''' + content_basic + '''</li>
		</ul>
    </body>
    </html>
    '''
    
@app.route('/')
def hello():
	return build_home_page()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5556)