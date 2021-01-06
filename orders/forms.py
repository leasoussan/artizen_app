from django import forms
from django.forms import ModelForm


from .models import Order, PaymentDetail, MessageBox

class CreateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('quantity', 'phone_number', 'email')



class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model= PaymentDetail
        fields = ('first_name_cc', 'last_name_cc', 'credit_card', 'expiration', 'digits_3')


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = MessageBox
        fields = ('subject', 'text')


class NewMessageForm(forms.ModelForm):
    class Meta:
        model = MessageBox
        fields = ('receiver','subject', 'text')        



class GuestMessageForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = MessageBox
        fields = ('subject', 'text')                