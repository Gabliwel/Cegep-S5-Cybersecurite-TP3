from flask import Flask, request, jsonify, make_response, render_template
import requests
import json
import jinja2

app = Flask('BackEnd')

def getInitialClientIP(request):
	print("trying to get IP", flush=True)
	ip = None

	if(request.data):
		if request.is_json:
			data = request.get_json()
			if 'ip' in data:
				ip = data['ip']
		else:
			print("not in json", flush=True)

	if ip == None:
		ip = request.remote_addr
	return ip


@app.route('/')
def hello():
	rep = dict()
	rep['message'] = "Welcome to the task API."
	ip = getInitialClientIP(request)
	rep['ip'] = ip

	print(str(rep), flush=True)
	return rep

@app.route('/test')
def hello2():
	return jsonify({'test':'bonsoir'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)