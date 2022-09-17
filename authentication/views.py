from django.shortcuts import render
from rest_framework import generics, response, status
from .serializers import RegisterSerializer

# sending email
from django.core.mail import send_mail, EmailMessage

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer= self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('serializer.save')

        user_data = serializer.data

        ''' sending email manualy'''
        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'info@sharpmind.club',
        #     ['o.perez1187@gmail.com'],
        #     fail_silently=False,
        # )
        ''' sending email with a templete'''
        msg = EmailMessage(
            from_email='info@sharpmind.club',
            to=['o.perez1187@gmail.com'],
        )
        # content
        title_mail = 'Perez'
        title_chess = 'my GM!'
        verify_my_email = "VERIFY!"
        my_site = "http://127.0.0.1:8000/"
        absurl = "http://127.0.0.1:8000/email-verify/?token=" # +str(token)


        msg.template_id = "d-c50d4fd610f944299e859d66d9d6201f"
        msg.dynamic_template_data = {
            "title": title_mail,
            "title_chess":title_chess,
            "verify_my_email":verify_my_email,
            "my_site":my_site,
            "verification_url":absurl,
        }
        msg.send(fail_silently=False)

        return response.Response(user_data, status=status.HTTP_201_CREATED)