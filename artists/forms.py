from django import forms 
from django.forms import ModelForm, ModelChoiceField
from .models import Item, City, Category, Country, Profile
from django.contrib.auth.models import User

class SearchArtistForm(forms.ModelForm):

    country = forms.ModelChoiceField(queryset= Country.objects.all().order_by('country'), initial = 'Israel')
    city = forms.ModelChoiceField(queryset=City.objects.filter(country__country='Afghanistan').order_by('city'))
    
    class Meta:
        model = Item
        fields = [
            'category',  'city'
        ]
        
  
class EditProfileUserForm(ModelForm):
    class Meta:
        model = User
        fields = (
                'email',
                'first_name',
                'last_name'
            )


class EditProfileForm(ModelForm):
    # country = forms.ModelChoiceField(queryset= Country.objects.all().order_by('country'), initial = "Select Country")
    # city = forms.ModelChoiceField(queryset=City.objects.filter(country__country='Afghanistan').order_by('city'))
    class Meta:
        model = Profile
        fields = ('category', 'country', 'city', 'location', 'bio', 'profile_pic', 'website', 'visite')



class AddItemForm(forms.ModelForm):
    """Form for the item model"""
    class Meta:
        model = Item
        fields = ('category', 'title', 'image', 'description', 'price')