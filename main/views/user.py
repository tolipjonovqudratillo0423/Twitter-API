from rest_framework.views import APIView
from main.utils import send_code
from django.contrib.auth import get_user_model
from main.models import User
from rest_framework.response import Response
from main.serializers import EmailSerializer
class SendEmail(APIView):

    serializer_class = EmailSerializer


    def post(self,request):
        
      
        
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = User.objects.create(email=email)

        code = user.create_code()

        send_code(email=email,code=code)

        data = {
            'status':True,
            'message':'Your Verification Code sent Succesfuly '
        }

        return Response(data)
    

class ConfirmVerificationCode(APIView):
    
    def post(self,request):

        pass