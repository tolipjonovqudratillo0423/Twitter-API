from django.contrib import admin
from main.models import User,UserConfirmation,Post
# Register your models here.


admin.site.register([User,UserConfirmation,Post])