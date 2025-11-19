import sqlite3
import bcrypt

DB_NAME = "users.db"
def db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE
        TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                PASSWORD TEXT NOT NULL
                )
                ''')
    conn.commit()
    conn.close()
    

def create_users():
    # first read through the passwords and users.txt
    with open("users.txt", "r") as user_txt:
        users = user_txt.readlines()
    with open("passwords.txt", "r") as password_txt:
        passwords = password_txt.readlines()
    
    for i in range(len(users)):
        curr_user = users[i].strip()
        curr_password = passwords[i].strip()
        register_user(curr_user, curr_password)
        print(f"{curr_user} registered with {curr_password}")


def register_user(user, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        hashed_password = hash_password(password)
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user, hashed_password,))
        conn.commit()
    except sqlite3.IntegrityError:
        print("User already exists")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cur.fetchone()
    conn.close()
    if result and check_password(password, result[0]):
        print("Login Successful")
        return True
    else:
        print("Invalid username or password")
        return False
    

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password)


def test():
    create_users()
    with open("users.txt", "r") as users_txt:
        users = users_txt.readlines()
    with open("passwords.txt", "r") as password_txt:
        passwords = password_txt.readlines()

    
    for i in range(len(users)):
        curr_user = users[i].strip()
        curr_password = passwords[i].strip()
        login_user(curr_user, curr_password)

db()
test()