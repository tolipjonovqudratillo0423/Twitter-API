from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import SendEmail,PostViewSet
from main.views import ConfirmVerificationCode,ResendCodeAPIView,LogInAPIView,SingUpAPIView


router = DefaultRouter()

router.register('post',PostViewSet,basename='post')

urlpatterns = router.urls

urlpatterns += [
    
    path('send_code/',SendEmail.as_view(),name='send_code'),
    path("verify_code/",ConfirmVerificationCode.as_view(),name='verify_code'),
    path("resend_code/",ResendCodeAPIView.as_view(),name='resend_code'),
    path("login/",LogInAPIView.as_view(),name='login'),
    path("signup/",SingUpAPIView.as_view(),name='signup')
]
