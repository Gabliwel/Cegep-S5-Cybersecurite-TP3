import sqlite3

def create_connection():
    db_file = './instance/users.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_faq(text, user_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.executescript("INSERT INTO faq (text, user_id) VALUES ('"+ text +"', '" + user_id +"')")
    conn.commit()
    conn.close()

def create_user(uuid, name, password, isAdmin):
    conn = create_connection()
    cur = conn.cursor()
    cur.executescript("INSERT INTO user (public_id, name, password, admin, cash_amount) VALUES ('"+ uuid +"', '" + name +"', '"+ password +"', False, 0)")
    conn.commit()
    conn.close()

def user_exists(public_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE public_id = '" + public_id + "'")

    result = cur.fetchall()
    data = {}
    index = 0
    #if len(result) > 0:
    for row in result:
        small_data = {}
        small_data['id'] = row[1]
        small_data['name'] = row[2]
        data[index] = small_data
        index+=1

    #responseLenght =len(cur.fetchall()[0])
    conn.close()
    return data
    #return bool(responseLenght > 0)
