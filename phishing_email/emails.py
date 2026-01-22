from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = message["Subject"]
    msg["From"] = message["From"]
    msg["To"] = message["To"]

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)



def email_interface():

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
            print("Please enter the name of the recipient: ")
            name = input()

            if not name:
                print("Please enter a valid name")
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
            name = input("Please enter the name of the recipient: ")
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
            
            name = input("Please enter the name of the recipient: ")
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