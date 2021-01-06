from django.shortcuts import render, HttpResponseRedirect, HttpResponse,redirect
from django.views import generic
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Category, City, Item
from artists.models import Profile
from django.urls import reverse_lazy
from .forms import SearchArtistForm, AddItemForm, EditProfileForm, EditProfileUserForm
from accounts.forms import MyUserCreationForm
from accounts.forms import CustomerCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.views import redirect_to_login
from django.db.models import Q
from accounts.decorators import check_profile
from django.contrib.auth.models import User
from orders.forms import GuestMessageForm

from termcolor import cprint
import json
import random 



def home_page(request):
    form = SearchArtistForm()
    products_query = Item.objects.all()[:10]
    context = {
    "form" : form,
    "products" : products_query,
    }
    return render(request, 'homepage.html', context)





class SearchResultsItems(ListView):
    model =Item
    context_object_name = 'results_list'
    template_name = 'artists/search_results.html'
    

    def get_queryset(self):
        countryquery = self.request.GET.get('country')
        categoryquery = self.request.GET.get('category') 
        cityquery = self.request.GET.get('city')
        cprint(f"city{cityquery}, category{categoryquery} ", 'red')
        results=  Item.objects.filter(
            Q(artist__city = cityquery) & Q(category = categoryquery) 
        ) 
        return results

        # Q(artist__country = countryquery) &         countryquery = self.request.GET.get('country')








@login_required
@user_passes_test(check_profile, login_url= '/create_profile/')
def my_profile(request):

    context = {
        
    'heading': "Welcome to Artizen - Complete Registration",
    }
    return render(request, 'artists/my_profile.html', context)







class CreateProfile(CreateView):
    model = Profile
    template_name = 'artists/edit_profile.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('my_profile_page')

    def get_initial(self):
        initial = super().get_initial()
        initial['country'] = 590
        return initial


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

   
def edit_Profile(request, pk):
    if request.method == 'POST':
        form = EditProfileUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('my_profile_page')
    else:
        form = EditProfileUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'artists/edit_profile.html', args)












# ----------------------------MIXIN UserPassesTestMixin

class ProfileCheckUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return check_profile(self.request.user)
    
    
    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return super().get_login_url()
        else:
            return '/create_profile/'

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())






class ItemView(DetailView):
    model = Item
    form_class = GuestMessageForm
    template_name = 'artists/item.html'





# Item Management ----------CRUD


class ItemDashBoard(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, ListView):
    model = Item
    template_name = 'artists/my_dashboard.html'
# showing item we want in the page
    def get_queryset(self):
        return Item.objects.filter(artist=self.request.user.profile)
    
#  the two below func make sure the user cant access if has not created a profile yet    
    




class EditItem(LoginRequiredMixin, ProfileCheckUserPassesTestMixin,  UpdateView):
    model = Item
    template_name = 'artists/edit_item.html'
    fields = ('category', 'title', 'image', 'description', 'price')
    success_url = reverse_lazy('my_dashboard')


    

class DeleteItem(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'artists/delete_item.html'
    success_url = reverse_lazy('my_dashboard')



@login_required
def add_item_form(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            artist = request.user.profile
            item = form.save(commit =False) 
            item.artist = artist
            item.save()
            return redirect('my_dashboard')
    else:
        form = AddItemForm()
    return render(request, 'artists/add_item.html', {'form': form})




# -------------------------------GUEST USER

def view_profile(request, pk):
    profile = profile = Profile.objects.get(pk=pk)
    items =  profile.item_set.all()[:4]
    context={
        'profile':profile,
        'items':items
    }

    return render(request, 'artists/artist_profile.html', context)




class ViewProfilePage(DetailView):
    pass        








# ajax

def load_cities(request):

    data = json.loads(request.body)
    cities = City.objects.filter(country_id=data['country_id']).order_by('city')
    city_list = json.dumps([(city.id, city.city) for city in cities])
    return HttpResponse(city_list)





# Above is the option 1
# class AddItem(LoginRequiredMixin, ProfileCheckUserPassesTestMixin, CreateView):
#     model =Item
#     template_name = 'artists/add_item.html'
    
#     fields = ('category', 'title', 'image', 'description', 'price')    


#     def form_valid(self, form):
#         artist = self.request.user.profile
#         item = form.save(commit =False) 
#         item.artist = artist
#         item.save()
#         return super().form_valid(form)
# 