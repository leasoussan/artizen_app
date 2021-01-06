from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.views import generic
from django.views.generic import CreateView 
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from artists.models import Profile
from accounts.forms import MyUserCreationForm, CustomerCreateForm
from django.contrib.auth.forms import UserCreationForm



from .mailers import send_welcome_signup 


class SignUpForm(View):
    def get(self, request):
        context = {
         "form": MyUserCreationForm()

        }
        return render(request, 'registration/signup.html', context)

    def post(self, request):
        form = MyUserCreationForm(request.POST)
        # user_type = request.POST('artist_profile', 'basic_profile')
        if form.is_valid():
            user = form.save() 
            user = authenticate(username= form.cleaned_data['username'], password =form.cleaned_data['password1'])
            
            if user is not None:
                login(request, user)
                send_welcome_signup(user)
                # this is ref to mailer 
            
                return redirect('create_profile')
        return render(request, 'registration/signup.html', {"form":form})      
