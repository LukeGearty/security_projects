import sqlite3
from datetime import datetime
import re

"""


Campaign Managmement portal


"""

DB = "emails.db"


def create_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                email_address TEXT UNIQUE NOT NULL,
                date_started TEXT NOT NULL,
                last_email_sent TEXT NOT NULL,
                is_clicked BOOLEAN
                
                )
                ''')
    
    con.commit()
    con.close()


def is_valid_date(date_string, format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False


def is_valid_email(email):
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    return bool(EMAIL_REGEX.match(email))


def start_campaign(name, email_address, date_started, last_email_sent, is_clicked=False):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    try:
        cur.execute('INSERT INTO users (name, email_address, date_started, last_email_sent, is_clicked) VALUES (?, ?, ?, ?, ?)', (name, email_address, date_started, last_email_sent, is_clicked))
        print(f"Campaign for {name} started")
        con.commit()
    except sqlite3.IntegrityError:
        print("User already in database")
    finally:
        con.close()


def start_campaign_interface():
    print("Enter the name of the employee: ")
    name = input()
    print("Enter the email address of the employee: ")
    email = input()
    
    
    while not is_valid_email(email):
        print("Invalid formation, please try again")
        email = input()


    print("Enter the date the campaign will start: ")
    print("Format: YYYY-MM-DD")
    
    start_date = input()
    
    while not is_valid_date(start_date):
        print("Invalid date format, please try again")
        start_date = input()
    print("Enter the date the email will be sent: ")
    print("Format: YYYY-MM-DD")
    last_email_sent = input()

    while not is_valid_date(last_email_sent):
        print("Invalid date format, please try again")
        last_email_sent = input()
    
    return name, email, start_date, last_email_sent


def get_user(name):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    user_info = cur.fetchall()

    con.close()
    return user_info


def get_users():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    users = cur.fetchall()
    con.close()
    names = []

    for user in users:
        names.append(user[1])
    return names


def check_campaign():
    users = get_users()

    for i, user in enumerate(users):
        print(f"{i + 1} : {user}")
    
    print("Which user do you want to check the campaign status of?")
    while True:
        try:
            choice = int(input())
        except ValueError:
            print("Invalid option, please select a number")
        
        break
    

    if choice > len(users) or choice <= 0:
        print("Invalid index position")
        return

    user_index = choice - 1
    
    user_info = get_user(users[user_index])
    print(user_info)
    print(f"User ID: {user_info[0][0]}")
    print(f"User Name: {user_info[0][1]}")
    print(f"Email Address: {user_info[0][2]}")
    print(f"Campaign Started: {user_info[0][3]}")
    print(f"Last Email Sent: {user_info[0][4]}")
    
    if not user_info[0][5]:
        print("User has not clicked on a phishing email")
    else:
        print("User has clicked on a phishing email")

    


def campaign_interface():
    create_db()
    print('\n' * 3)
    while True:
        print(" ++ Phishing Campaign Interface ++ ")
        print("1. Enter a new user")
        print("2. Check Status of a user")
        print("3. Exit")
        try:
            choice = int(input())
        except ValueError:
            print("Enter a number as your choice")


        if choice == 1:
            name, email_address, date_started, last_email_sent = start_campaign_interface()
            start_campaign(name, email_address, date_started, last_email_sent)
        elif choice == 2:
            check_campaign()

            print('\n'*3)
        elif choice == 3:
            break
        
        else:
            print("Invalid Choice")
