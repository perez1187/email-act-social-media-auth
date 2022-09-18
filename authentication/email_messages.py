from django.core.mail import send_mail, EmailMessage
from decouple import config

def register_sendgrid(receiver):
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
        to=[receiver],
    )
    # # content
    title_mail = 'Perez'
    title_chess = 'my GM!'
    verify_my_email = "VERIFY!"
    my_site = "http://127.0.0.1:8000/"
    absurl = "http://127.0.0.1:8000/email-verify/?token=" # +str(token)
    msg.template_id = config("TEMPLATE_ID")
    
    # sending data:
    msg.dynamic_template_data = {
        "title": title_mail,
        "title_chess":title_chess,
        "verify_my_email":verify_my_email,
        "my_site":my_site,
        "verification_url":absurl,
    }
    msg.send(fail_silently=False)