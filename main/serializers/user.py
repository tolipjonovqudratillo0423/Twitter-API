from rest_framework import serializers 
from main.models import User
from rest_framework.serializers import ModelSerializer
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True,max_length=100)
    
    def validate_email(self,email):
        if User.objects.filter(email=email).exists() and User.objects.filter(email=email).filter(status='verified'):
            raise serializers.ValidationError('Email already exists')
        
        if email is None:
            raise serializers.ValidationError('Email is required')  
        
        
        return email
    
class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
