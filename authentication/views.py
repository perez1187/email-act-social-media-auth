from django.shortcuts import render
from rest_framework import generics, response, status
from .serializers import RegisterSerializer

# sending email
from django.core.mail import send_mail, EmailMessage

from .email_messages import register_sendgrid as authentication_register_sendgrid

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer= self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        #serializer.save()
        #print(user['email'])
        user_data = serializer.data

        # sending registration email
        receiver =user["email"]
        authentication_register_sendgrid(receiver)

        return response.Response(user_data, status=status.HTTP_201_CREATED)



    