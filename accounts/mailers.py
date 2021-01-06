from django.conf import settings 
from django.core.mail import send_mail 



def send_welcome_signup(user):
    subject = f'welcome {user}to Artizen '
    message = f'Hi {user}, thank you for registering To ArtiZen.'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user.email,] 
    print(recipient_list)
    send_mail(subject, message, email_from, recipient_list, fail_silently = False ) 


def send_order_confirmation(payment):
    subject = f'Your Payment Confirmation  is #{payment.id} Thank youf for buying with us.....ARTiZEN'
    message = f'Hi {payment.buyer.user.username}, thank you for purchassing Local Artist @ ArtiZen. please see below the details of your Order '
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [payment.buyer.user.email, ] 
    send_mail( subject, message, email_from, recipient_list, fail_silently = False ) 


def send_message(user, subject, text):
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user.email, ] 
    send_mail( subject, text, email_from, recipient_list,fail_silently = False ) 
    

def guest_message_confirmation(message):
    subject = f'Your Message to {message.email} was sent'
    text = f'Hi, thank you for your interest we will get back to you shortly'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [message.email, ] 
    send_mail(subject, text, email_from, recipient_list ,fail_silently = False) 