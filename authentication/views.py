from rest_framework import generics, response, status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# local
from .serializers import RegisterSerializer as authentication_Register_Serializer
from .email_messages import register_sendgrid as authentication_register_sendgrid
from .models import User

class RegisterView(generics.GenericAPIView):

    serializer_class = authentication_Register_Serializer

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

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass

    