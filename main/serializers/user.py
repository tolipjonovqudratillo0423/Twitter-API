from rest_framework import serializers 
from main.models import User,StatusChoices
from main.utils import is_email,is_valid_username

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True,max_length=100)
    
    def validate_email(self,email):
        
        if is_email(email):
            if User.objects.filter(email = email).exists():
                raise serializers.ValidationError('Email have already taken')
            else:
                return email
        
        if email is None:
            raise serializers.ValidationError('Email is required')  
        
        raise serializers.ValidationError('Please, Enter Valid email !')
        
       
    
class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 20)
    confirm_password = serializers.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','phone','password','confirm_password']


    def validate(self, value):

        password = value.get('password')
        confirm_password = value.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('You password and confirm_password is diffrent')
        
        return value
    

    def validate_phone(self,value):

        phone = value

        if len(phone) != 13:
            raise serializers.ValidationError('Please. Enter valid phone number of Uzbekistan')
        
        return value
    


    def validate_username(self, value):

        user_input = value

    
        if is_valid_username(username=user_input):

            if User.objects.filter(username = user_input).exists():
                raise serializers.ValidationError('Username have already taken')
            else:
                return value
            
        else:
            raise serializers.ValidationError('Please. Enter valid username or email on field user_input !!!')
        
        
    

    def update(self, instance, validated_data):
        
        password = validated_data.pop('password',None)
        validated_data.pop('confirm_password',None)

        for attrs, value in validated_data.items():
            setattr(instance,attrs,value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 50)
    password = serializers.CharField(max_length = 20)
    
    

    def validate(self, value):

        user_input = value.get('username')

        if is_email(user_input):
            user =  User.objects.filter(email = user_input).filter(status = StatusChoices.DONE).first()
    
            if user is not None:
                value['username'] = user.username
            else:
                raise serializers.ValidationError('User not found')    
        else:
            value['username'] = user_input
    
        return value

    

    




        

        

    

