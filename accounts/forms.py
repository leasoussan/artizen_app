from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from artists.models import Profile


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']




class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Profile 
        exclude = ['user'] 

    
class UserCustomerCreateForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = ['city', 'country', 'phone_number'] 