from celery import shared_task
from django.template.loader import render_to_string  

from .send_email import send_email
from .token import account_activation_token

@shared_task
def send_confirmation_email(user):
    mail_subject = 'Activation link has been sent to your email id'  
    current_site = "http://127.0.0.1:8000"
    message = render_to_string('acc_active_email.html', {  
                'user': user['email'],  
                'uid':user['id'],
                'domain': current_site,
                'token':account_activation_token.make_token(user),
    })

    send_email({"domain":current_site, "to_user":user['email'], "subject":mail_subject, "body":message})
    return "Email sent to {}".format(user['email'])