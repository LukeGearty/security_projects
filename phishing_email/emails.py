from jinja2 import Template


def render_email(base_path, body_path, context):
    with open(body_path) as f:
        body = Template(f.read()).render(context)

    with open(base_path) as f:
        base = Template(f.read())
    
    return base.render(
        content=body,
        footer="" # TODO
    )



def password_reset_email(name, email):
    html = render_email(
        "templates/base.html",
        "templates/password_reset.html",
        {
            "name": name,
            "email": email,
            "link": "https",
            "tracking_pixel": '<img scr="https://www.example.com" width="1" height="1">'
        }
    )
    return html



def meeting_email(name, email):
    pass



def mfa_email(name, email):
    pass


def email_interface():
    pass