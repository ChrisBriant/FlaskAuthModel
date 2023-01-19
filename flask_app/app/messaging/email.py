from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import os

TEMPLATES = {
    'GENERAL_CONFIRM_EMAIL' : 'd-92a9d2157e124529b61677f459018eff',
    'GENERAL_RESET_EMAIL' :'d-591230395b87478e9d239c19f68d3631',
}

def send_password_reset_email(emailad, name, url):
    from_email = os.environ.get('SENDGRID_FROM_ADDRESS')
    to_email = emailad
    mail = Mail(from_email=from_email, to_emails=to_email)
    mail.template_id = TEMPLATES['GENERAL_RESET_EMAIL']
    mail.dynamic_template_data = {
        'confirm_url': url,
        'username': name
    }
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mail)
        return response
    except Exception as e:
        print(e)


def send_confirm_email(emailad,username,url):
    from_email = os.environ.get('SENDGRID_FROM_ADDRESS')
    to_email = emailad
    mail = Mail(from_email=from_email, to_emails=to_email)
    mail.template_id = TEMPLATES['GENERAL_CONFIRM_EMAIL']
    mail.dynamic_template_data = {
        'confirm_url': url,
        'username' : username,
    }
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mail)
        return response
    except Exception as e:
        print(e)

