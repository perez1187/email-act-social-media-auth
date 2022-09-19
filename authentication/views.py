from logging import raiseExceptions
from rest_framework import generics, response, status, views
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

# local
from .serializers import RegisterSerializer,EmailVerificationSerializer, LoginSerializer
from .email_messages import register_sendgrid as authentication_register_sendgrid
from .models import User
from .renders import UserRenderer

# 3rd part
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        # save user to db
        user = request.data
        serializer= self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # create token for User      
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        # # sending registration email
        current_site = get_current_site(request).domain
        relative_link=reverse('email-verify') # relative name urls.py
        absurl = 'http://'+current_site +relative_link+"?token="+str(token)
        
        email_body = 'hi' # I use template

        data = {
            "receiver":user_data["email"],
            "domain":absurl,
            "subject": 'Verify Email',
        }
        authentication_register_sendgrid(data)

        return response.Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description my', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config]) # create data for swagger
    def get(self,request):
        token = request.GET.get('token') # take token from url

        # try to decode, secret key from settings (this projet secret key)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return response.Response({'email':'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return response.Response({'error':'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return response.Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)