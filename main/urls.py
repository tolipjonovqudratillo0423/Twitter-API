from django.urls import path
from main.views import SendEmail
urlpatterns = [
    path('send_code/',SendEmail.as_view(),name='send_code'),
]