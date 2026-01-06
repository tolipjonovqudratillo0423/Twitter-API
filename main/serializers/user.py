from rest_framework import serializers 
from main.models import User
from rest_framework.serializers import ModelSerializer
from main.utils import is_email,is_valid_username

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

class UserSerializer(serializers.ModelSerializer):
    user_input = serializers.CharField(max_length = 50)
    password = serializers.CharField(max_length = 20)
    confirm_password = serializers.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['user_input','first_name','last_name','phone','password','confirm_password']

    
    def validate_user_input(self, value):

        user_input = value

        if is_email(user_input):
            if User.objects.filter(email = user_input).exists():
                raise serializers.ValidationError('Email have already taken')
            
        elif is_valid_username(username=user_input):
            if User.objects.filter(username = user_input).exists():
                raise serializers.ValidationError('Username have already taken')
            
        if is_email(user_input) == False and is_valid_username(user_input) == False:
            raise serializers.ValidationError('Please. Enter valid username or email on field user_input !!!')
        
        return value
    

    def validate_phone(self,value):

        phone = value

        if len(phone) != 13:
            raise serializers.ValidationError('Please. Enter valid phone number of Uzbekistan')
        
        return value
    

    def validate(self, value):

        password = value.get('password')
        confirm_password = value.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('You password and confirm_password is diffrent')
        
        return value

        





        

        

    

