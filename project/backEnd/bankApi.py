from flask import Flask, request, jsonify, make_response
import uuid
import datetime
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask("bankAPI")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./users.db'
db = SQLAlchemy(app)

app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] = True
flask_bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    cash_amount = db.Column(db.Float)

def wrap_user_in_dict(user):
    user_data = {}
    user_data['id'] = user.id
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['cash_amount'] = user.cash_amount
    return user_data

def generate_password_hash(password):
    return flask_bcrypt.generate_password_hash(password, 13).decode()

def get_initial_client_ip(request):
    ip = None
    if(request.data):
        if request.is_json:
            data = request.get_json()
            if 'ip' in data:
                ip = data['ip']
        else:
            print('not in json', flush = True)
    
    if ip == None:
        ip = request.remote_addr
    
    return ip

@app.route('/')
def welcomePage():
    rep = dict()
    rep['message'] = "Welcome to your favourite bank service ! :)"
    return rep

@app.route('/login')
def login():
    ip = get_initial_client_ip(request)

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message' : 'Could not authenticate you'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return jsonify({'message' : 'Could not authenticate you'})
    
    if flask_bcrypt.check_password_hash(user.password, user.password):
        return jsonify({'message' : 'You are authenticated from ' + ip + 'Welcome user : ' + user.name})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    if len(sys.argv) > 2:
        print("To many arguments : need 2")
    elif len(sys.argv) == 2:
        hashed_password = generate_password_hash(sys.argv[1])
        new_user = User(public_id=str(uuid.uuid4()), name='Admin', password=hashed_password, admin=True)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
    elif len(sys.argv) == 1:
        app.run(debug=True, host='0.0.0.0', port=5555)