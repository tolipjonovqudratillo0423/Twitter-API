from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.utils import timezone
import string
import random

class StatusChoices(models.TextChoices):
    NEW ,VERIFIED ,DONE = (('new',"New"),('verified','Verified'),('done','Done'))




class User(AbstractUser):
    username = models.CharField(max_length=100,blank=True,null = True,unique=True)
    phone = models.CharField(max_length=13,unique=True,null=True,blank=True)
    status = models.CharField(choices=StatusChoices,default=StatusChoices.NEW)
    bio = models.TextField()
    image = models.ImageField(upload_to='user/')

    def __str__(self):
        return self.username
    
    def create_code(self ):
        
        code = ''.join(random.choice(string.digits) for _ in range(6))

        UserConfirmation.objects.create(
            user = self,
            code = code
        )
        return code

    
    def save(self,*args,**kwargs):

        if not self.username:
            self.username = str(uuid4()).split('-')[-1]
        if not self.password:
            self.password = str(uuid4()).split('-')[-1]

        return super().save(*args,**kwargs)
    


class UserConfirmation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self,*args,**kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        return super().save(*args,**kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f'{self.user.username} - {self.code}'