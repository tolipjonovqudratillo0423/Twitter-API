from rest_framework.views import APIView
from main.utils import send_code
from django.contrib.auth import get_user_model
from main.models import User,UserConfirmation,StatusChoices
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from main.serializers import EmailSerializer,CodeSerializer
from rest_framework.permissions import IsAuthenticated

class SendEmail(APIView):

    serializer_class = EmailSerializer


    def post(self,request):
        
      
        
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        user = User.objects.create(email=email)

        code = user.create_code()

        send_code(email=email,code=code)

        refresh = RefreshToken.for_user(user)
        data = {
            'status':True,
            'message':'Your Verification Code sent Succesfuly ',
            'token':{
                'access':str(refresh.access_token),
                'refresh':str(refresh)
            },
            
        }

        return Response(data)
    

class ConfirmVerificationCode(APIView):
    serializer_class=CodeSerializer
    def post(self,request):

        serializer=CodeSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        if len(code) < 6:
            return Response({
                'status':False,
                'message':'Your Verification Code is too short !!! '

            })
        

        try:
            user_confirmation = UserConfirmation.objects.get(code=code)
        except UserConfirmation.DoesNotExist:
            return Response({'message':'Invalid code'},status=status.HTTP_400_BAD_REQUEST)

        if UserConfirmation.is_expired(user_confirmation):
            return Response({'message':'Code expired'},status=status.HTTP_400_BAD_REQUEST)

        user_confirmation.user.status = StatusChoices.VERIFIED
        user_confirmation.user.save()
        user_confirmation.delete()

        return Response({'message':'Code confirmed'},status=status.HTTP_200_OK)


