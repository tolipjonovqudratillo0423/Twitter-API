from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string 
from django.conf import settings
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import re
from django.shortcuts import redirect

def redirector(request):
    return redirect('swagger-ui')

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
 
def tokens(user):

    refresh = RefreshToken.for_user(user)

    data = {
        'token':{
            'access':str(refresh.access_token),
            'refresh':str(refresh)
        }
    }

    return data

def is_email(email):
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_username(username):
    """
    Validates a username according to the following rules:
    1. Between 4 and 25 characters long.
    2. Must start with a letter.
    3. Can only contain letters, numbers, and the underscore character.
    4. Cannot end with an underscore character.
    """
    # Regex pattern explained:
    # ^[a-zA-Z]      - Starts with a letter
    # [a-zA-Z0-9_]{2,23} - Followed by 2 to 23 letters, numbers, or underscores
    # [a-zA-Z0-9]    - Ends with a letter or number (ensures no trailing underscore)
    # $              - End of the string
    # Total length will be between 1+2+1=4 and 1+23+1=25 chars
    pattern = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{2,23}[a-zA-Z0-9]$")

    return bool(pattern.match(username))


class ResponseMessage():

    @staticmethod

    def success(message:str, data:dict = None)->dict:

        return Response({
            'status':True,
            'message':message,
            'data':data,
        },status=status.HTTP_200_OK)
    
    @staticmethod
    
    def error(message:str, data:dict = None)->dict:

        return Response({
            'status':False,
            'message':message,
            'data':data,
        },status=status.HTTP_406_NOT_ACCEPTABLE)

    


