import sqlite3

def create_connection():
    db_file = './users.db'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
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
    cur.executescript("INSERT INTO user (public_id, name, password, admin) VALUES ('"+ uuid +"', '" + name +"', '"+ password +"', False)")
    conn.commit()
    conn.close()

def user_exists(user_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.executescript("SELECT * FROM user WHERE id = " + user_id)

    responseLenght =len(cur.fetchall()[0])
    conn.commit()
    conn.close()
    return bool(responseLenght > 0)