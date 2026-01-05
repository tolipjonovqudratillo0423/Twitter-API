from django.urls import path
from main.views import SendEmail
from main.views import ConfirmVerificationCode

urlpatterns = [
    path('send_code/',SendEmail.as_view(),name='send_code'),
    path("verify_code/",ConfirmVerificationCode.as_view(),name='verify_code')
]