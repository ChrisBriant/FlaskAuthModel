from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import os

TEMPLATES = {
    'GENERAL_CONFIRM_EMAIL' : 'd-92a9d2157e124529b61677f459018eff',
    #'GENERAL_RESET_EMAIL' :'d-0dd3d3019efd4a22995899ee85a6440e',
}

# def send_password_reset_email(emailad, name, url):
#     from_email = settings.ADMIN_SMTP
#     to_email = emailad
#     mail = Mail(from_email=from_email, to_emails=to_email)
#     mail.template_id = TEMPLATES['ADVENT_RESET_EMAIL']
#     mail.dynamic_template_data = {
#         'confirm_url': url,
#         'username': name
#     }
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(mail)
#         return response
#     except Exception as e:
#         print(e)


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


# def send_calendar_link(emailad,name,img_name,img_url,advent_url):
#     from_email = settings.ADMIN_SMTP
#     to_email = emailad
#     mail = Mail(from_email=from_email, to_emails=to_email)
#     mail.template_id = TEMPLATES['ADVENT_SHARE_LINK']
#     mail.dynamic_template_data = {
#         'name' : name,
#         'img_name' : img_name,
#         'img_url' : img_url,
#         'advent_url' : advent_url
#     }
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(mail)
#         return response
#     except Exception as e:
#         print(e)


# def send_message_to_me(name,message_text):
#     from_email = settings.ADMIN_SMTP
#     to_email = settings.AUTHOR_SMTP
#     mail = Mail(from_email=from_email, to_emails=to_email)
#     mail.template_id = TEMPLATES['ADVENT_SEND_TO_ME']
#     mail.dynamic_template_data = {
#         'user' : name,
#         'message_text' : message_text,
#     }
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(mail)
#         return response
#     except Exception as e:
#         print(e)

