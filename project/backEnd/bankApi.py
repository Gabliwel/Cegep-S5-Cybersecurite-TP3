from flask import Flask, request, jsonify, make_response
import hashlib
import uuid
import datetime
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import dbHandler

app = Flask("bankAPI")

app.config['SECRET_KEY'] = 'super secret key'
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

class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    user_id = db.Column(db.String(50))

def wrap_user_in_dict(user):
    user_data = {}
    user_data['id'] = user.id
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['cash_amount'] = user.cash_amount
    return user_data

def wrap_faq_message_in_dict(faq):
    faq_data = {}
    faq_data['id'] = faq.id
    faq_data['text'] = faq.text
    faq_data['user_id'] = faq.user_id
    return faq_data

def generate_password_hash(password):
    hash = hashlib.md5(password.encode())
    return hash.hexdigest()
    #return flask_bcrypt.generate_password_hash(password, 13).decode()

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

def get_user_from_token(token):
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if not token:
        print('not token', flush = True)
        raise ValueError('Token is missing.')
    
    try:
        print(token, flush = True)
        print(app.config['SECRET_KEY'], flush = True)
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except Exception as e:
        print(str(e), flush = True)
        raise ValueError('Token is invalid.')
    
    user_id = data['user_id']
    return User.query.filter_by(id=user_id).first()

@app.route('/')
def welcomePage():
    rep = dict()
    rep['message'] = "Welcome to your favourite bank service ! :)"
    return rep

@app.route('/login',  methods=['POST'])
def login():
    ip = get_initial_client_ip(request)

    auth = request.authorization
    print(auth, flush=True)
    if not auth or not auth.username or not auth.password:
        return jsonify({'message' : 'Could not authenticate you'}), 401

    user = User.query.filter_by(name=auth.username).first()
    print(user.id, flush=True)
    print(wrap_user_in_dict(user), flush=True)
    if not user:
        return jsonify({'message' : 'Could not authenticate you'}), 401
    
    #if flask_bcrypt.check_password_hash(user.password, auth.password):
    if user.password == generate_password_hash(auth.password):
        token = jwt.encode({'user_id':user.id}, app.config['SECRET_KEY'], algorithm="HS256")
        print(token, flush=True)
        return jsonify({'message' : 'You are authenticated from ' + ip + '. Welcome user : ' + user.name, 'token': token})
    
    return jsonify({'message' : 'Could not authenticate you'}), 401


@app.route('/user', methods=['POST'])
def create_user():
    try:
        current_user = get_user_from_token(request)
    except Exception as e:
        return jsonify({'message': str(e)}), 401
    
    if current_user.admin:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        dbHandler.create_user(str(uuid.uuid4()), data['name'], hashed_password, False)
        return jsonify({'message' : 'New user created'})

    return jsonify({'message' : 'Access denied'})

@app.route('/user', methods=['GET'])
def view_user():

    try:
        current_user = get_user_from_token(request)
    except Exception as e:
        return jsonify({'message': str(e)}), 401
    
    if current_user:
        rep = dict()
        rep['message'] = 'Bonjour ' + current_user.name
        rep['public_id'] = current_user.public_id
        rep['solde'] = str(current_user.cash_amount) + '$'
        if current_user.name == 'Gandalf':
            rep['JWT'] = 'FLAG-5555555555'
        elif current_user.name == 'Pippin':
            rep['Hash)'] = 'FLAG-3333333333'
        elif current_user.name == 'Saruman':
            rep['CSRF)'] = 'FLAG-1111111111'

        return rep
    return jsonify({'message': 'Access denied.'})

@app.route('/search', methods=['POST'])
def search_user():
    if(request.data):
        if request.is_json:
            data = request.get_json()
            if 'searchTerm' in data:
                search = request.json['searchTerm']
                print(str(search), flush=True)
                output = dbHandler.user_exists(search)
                return jsonify({'search':output})
                '''
                count = User.query.filter_by(name=search).count()
                if count == 0:
                    return jsonify({'message' : search + ' n existe pas'})
                else:
                    return jsonify({'message' : search + ' existe'})
                '''
    return jsonify({'message' : 'Une erreur est survenu'})

@app.route('/transfert', methods=['POST'])
def transfer():
    try:
        current_user = get_user_from_token(request)
    except Exception as e:
        return jsonify({'message': str(e)}), 401

    if not current_user:
        return jsonify({'message': 'Access denied.'})

    data = request.get_json()
    amountStr = data['amount']
    receiver = data['account']
    amount = None

    try:
        amount = float(amountStr)
    except Exception as e:
        return jsonify({'message': 'Invalid amount'})

    if current_user.cash_amount - amount < 0:
        return jsonify({'message': 'Not enough money to transfer ' + str(amount) + '$'})

    user2 = User.query.filter_by(name=receiver).first()
    if not user2:
        return jsonify({'message' : receiver + ' n existe pas'})

    #donc cest possible
    User.query.filter_by(name=receiver).update(dict(cash_amount=(user2.cash_amount+amount)))
    db.session.commit()

    User.query.filter_by(id=current_user.id).update(dict(cash_amount=(current_user.cash_amount-amount)))
    db.session.commit()

    return jsonify({'message' : 'Transfert complété!'})

@app.route('/faq', methods=['POST'])
def create_faq():
    try:
        current_user = get_user_from_token(request)
    except Exception as e:
        return jsonify({'message': str(e)}), 401

    if current_user:
        data = request.get_json()
        new_faq = Faq(text=data['message'], user_id=current_user.id)
        db.session.add(new_faq)
        db.session.commit()
        return jsonify({'faq':'Message ajouté!'})
    return jsonify({'message': 'Access denied.'})

@app.route('/faq', methods=['GET'])
def viewFaq():
    try:
        current_user = get_user_from_token(request)
    except Exception as e:
        return jsonify({'message': str(e)}), 401
    
    if current_user:
        faqElements = Faq.query.all()
        output = []
        print(faqElements, flush = True)
        for e in faqElements:
            output.append(wrap_faq_message_in_dict(e))
        print(output, flush = True)
        return jsonify({'faq':output})
    return jsonify({'message': 'Access denied.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
 
    if len(sys.argv) > 2:
        print("To many arguments : need 2")
    elif len(sys.argv) == 2:
        hashed_password = generate_password_hash(sys.argv[1])
        new_user_boromir = User(public_id=str(uuid.uuid4()), name='Boromir', password=hashed_password, admin=True, cash_amount = 0)
        new_user_flag = User(public_id=str(uuid.uuid4()), name='FLAG-2222222222', password=hashed_password, admin=False, cash_amount = 0)
        new_user_gandalf = User(public_id=str(uuid.uuid4()), name='Gandalf', password=hashed_password, admin=False, cash_amount = 800)
        hashed_password = generate_password_hash("qwerty")
        new_user_pippin = User(public_id=str(uuid.uuid4()), name='Pippin', password=hashed_password, admin=False, cash_amount = 300)
        new_faq = Faq(text="Promotion de fin session", user_id=1)
        new_faq2 = Faq(text="La promo de l'année!", user_id=1)

        with app.app_context():
            #clean up
            User.query.delete()
            Faq.query.delete()
            db.session.commit()

            #default user
            db.session.add(new_user_boromir)
            db.session.add(new_user_flag)
            db.session.add(new_user_gandalf)
            db.session.add(new_user_pippin)

            db.session.add(new_faq)
            db.session.add(new_faq2)
            db.session.commit()
        app.run(debug=True, host='0.0.0.0', port=5555)
    elif len(sys.argv) == 1:
        app.run(debug=True, host='0.0.0.0', port=5555)