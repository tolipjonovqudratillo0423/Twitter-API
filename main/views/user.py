from rest_framework.views import APIView
from main.utils import send_code,ResponseMessage,tokens
from django.contrib.auth import get_user_model
from main.models import User,UserConfirmation,StatusChoices
from rest_framework.response import Response
from rest_framework import status
from main.serializers import EmailSerializer,CodeSerializer,UserSerializer
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

        token = tokens(user)
        data = {
            'status':True,
            'message':'Your Verification Code sent Succesfuly ',
            'token':token
            
        }

        return Response(data)
    

class ConfirmVerificationCode(APIView):

    permission_classes = [IsAuthenticated,]
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

    
class ResendCodeAPIView(APIView):

    def post(self,request):

        user = request.user

        if self.resend_code(user):
            return ResponseMessage.success(
                message='Your Verification Code sent Successfully')
        else:
            return ResponseMessage.error(
                message='You have got unexpired code or You have already VERIFIED'
            )
        
    def resend_code(self,user):
        
        confirmation = user.confirmations.order_by('-created_at').first()

        if confirmation.is_expired() and user.status == StatusChoices.NEW:
            code = user.create_code()
            send_code(email=user.email,code=code)
            return True
        return False
    




class SingUpAPIView(APIView):   

    serializer_class = UserSerializer

    def post(self,request):
        user = request.user

        serializer = self.serializer_class(user,data = request.data)

        serializer.is_valid(raise_exception=True)
        user.save()

        return ResponseMessage.success(message='User Updated Successfully')

        