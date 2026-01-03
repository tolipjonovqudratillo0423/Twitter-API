from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
def send_code(email:str,code:int):

    text = f'You confiramtion code from X.com ===> {code} <==='

    send_mail(
        "Verification Code",
        text,
        EMAIL_HOST_USER,
        email,

    )

