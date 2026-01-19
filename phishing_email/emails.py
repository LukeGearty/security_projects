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
    pass
