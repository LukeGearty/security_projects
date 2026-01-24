import sqlite3
from datetime import datetime
import re
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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


def get_user_name():
    # for when you just need the name

    #get all the users
    users = get_users()
    if not users:
        print("No users in this database, please add")
        return

    print("Which user is this email for?: ")
    for i,user in enumerate(users):
        print(f"{i + 1} : {user}")
    while True:
        try:
            choice = int(input())
        except ValueError:
            print("Invalid option, please select a number")
        break
    if choice < 0 or choice > len(users):
        print("invalid Choice")
        return
    
    user_index = choice - 1
    name = users[user_index]
    return name


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
    
    if len(users) == 0:
        print("No current users active, please add")
        return
    

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


"""

Edit when last email was sent

Update whether user has clicked on a phishing email

"""

def update_last_email_sent(user, updated_date):
    """
    
    Query the database
        UPDATE users SET last_email_sent = ? WHERE name = ?
        
    """
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("UPDATE users SET last_email_sent = ? WHERE name = ?", (user, updated_date))
    con.commit()
    con.close()



def update_user_has_clicked(user):
    # Kind of just a toggle
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("UPDATE users SET is_clicked = NOT is_clicked WHERE name = ?", (user,))
        
    con.commit()
    con.close()
    # TODO add a better UX option, right now it is a little too mysterious


def update_user_interface():
    print('\n' * 3)
    name = get_user_name()
    if not name:
        print("Error with that user name, exiting")
        return
    

    while True:
        print(f" -- Updating {name} Information -- ")
        print("1. Update Last Email Sent")
        print("2. Update whether user had clicked on a phishing link")
        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number as a choice")
        
        if choice == 1:
            print("Please enter the date of the last email sent in YYYY-MM-DD format: ")
            date = input()

            while not is_valid_date(date):
                print("Please enter a date in the valid format: ")
                date = input()
            
            update_last_email_sent(name, date)
            return
        elif choice == 2:
            update_user_has_clicked(name)
            return
        else:
            print("Pleae enter a valid choice")

        


def campaign_interface():
    create_db()
    print('\n' * 3)
    while True:
        print(" ++ Phishing Campaign Interface ++ ")
        print("1. Enter a new user")
        print("2. Check Status of a user")
        print("3. Create an email for a user")
        print("4. Update an user's information")
        print("5. Exit")
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
            email_interface()
            print("Please edit the html as you see fit")
            print('\n'*3)
        elif choice == 4:
            update_user_interface()
        elif choice == 5:
            break
        
        else:
            print("Invalid Choice")



"""

Email management functions

"""


def render_email(base_path, body_path, context):
    with open(body_path) as f:
        body = Template(f.read()).render(context)

    with open(base_path) as f:
        base = Template(f.read())
    
    return base.render(
        content=body,
        footer="" # TODO
    )



def password_reset_email(name, link):
    html = render_email(
        "templates/base.html",
        "templates/password_reset.html",
        {
            "name": name,
            "link": link,
        }
    )
    return html



def meeting_email(name, meeting_link, meeting_title, meeting_date, meeting_time, organizer):
    html = render_email("templates/base.html",
                        "templates/meeting.html",
                        {
                            "name": name,
                            "meeting_title": meeting_title,
                            "meeting_link": meeting_link,
                            "meeting_date": meeting_date,
                            "meeting_time": meeting_time,
                            "organizer": organizer
                        })
    return html


def mfa_email(name,location, device, timestamp, verify_link):
    html = render_email("templates/base.html",
                        "templates/meeting.html",
                        {
                            "name": name,
                            "location": location,
                            "device": device,
                            "timestamp": timestamp,
                            "verify_link": verify_link,
                        })
    return html


def send_email(message, html_body):
    """
    message: dictionary
        "Subject" 
        "From"
        "To":

    Will try to implement this last
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = message["Subject"]
    msg["From"] = message["From"]
    msg["To"] = message["To"]

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)



def email_interface():
    
    name = get_user_name()

    if not name:
        print("Error with that user, exiting")
        return

    print(f"Creating a campaign for {name}")
    
    while True:
        print(" == Email Creation == ")
        print("What kind of email would you like to create: ")
        print("1. Password Reset")
        print("2. Meeting Notification")
        print("3. MFA Notification")

        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number as your choice")
        
        
        if choice == 1:
            # Password reset
            print("Please enter a link for the recipient to click: ")
            link = input()

            if not link: 
                print("Please enter a valid link")

            if name and link:
                email_html = password_reset_email(name, link)

                with open('password_reset.html', 'w') as f:
                    f.write(email_html)
        
            return
        elif choice == 2:
            # Meeting email
            # TODO: Figure out a better way to do this and validate input
            meeting_link = input("Please enter a  meeting link: ")
            meeting_title = input("Please enter the title of the meeting: ")
            meeting_date = input("Please enter a date: ")
            meeting_time = input("Please enter a time: ")
            organizer = input("Please enter the organizer: ")
            
            email_html = meeting_email(name, meeting_link, meeting_title, meeting_date, meeting_time, organizer)

            with open("meeting.html", "w") as f:
                f.write(email_html)
            
            return
        elif choice == 3:
            # MFA email
            location = input("Please enter a location: ")
            device = input("Please enter a device: ")
            timestamp = input("Please enter a timestamp: ")
            verify_link = input("Please enter a verification link: ")

            email_html = mfa_email(name,location, device, timestamp, verify_link)

            with open("email_html", "w") as f:
                f.write(email_html)

            return
        else:
            print("Invalid choice, please choose again")


def main():
    while True:
        print("== PHISHING TRAINING MAIN MENU INTERFACE ==")
        print('\n' * 2)
        print("1. Campaign Menu ")
        print("2. Exit")

        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number as your selection")
        if choice == 1:
            campaign_interface()
        elif choice == 2:
            break
        else:
            print("Invalid choice")
    

if __name__=="__main__":
    main()