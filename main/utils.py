from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string 
from django.conf import settings
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
def send_code(email:str,code:int):

    text = f'You confiramtion code from X.com ===> {code} <==='

    html_message = render_to_string(
        'email_message.html',
        {
            'code':code
        }
    )

    send_mail(
        subject="Verification Code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email,],
        html_message=html_message

    )

