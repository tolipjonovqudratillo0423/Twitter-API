from django.urls import path
from main.views import SendEmail
from main.views import ConfirmVerificationCode,ResendCodeAPIView,LogInAPIView,SingUpAPIView

urlpatterns = [
    path('send_code/',SendEmail.as_view(),name='send_code'),
    path("verify_code/",ConfirmVerificationCode.as_view(),name='verify_code'),
    path("resend_code/",ResendCodeAPIView.as_view(),name='resend_code'),
    path("login/",LogInAPIView.as_view(),name='login'),
    path("signup/",SingUpAPIView.as_view(),name='signup')
]