from django.conf import settings 
from django.db import models
from django.urls import reverse


from django.contrib.auth.models import User



CURRENCY = settings.CURRENCY


class Country(models.Model):
    country = models.CharField(max_length = 50)

    class Meta:
        ordering = ['country']
        
    def __str__(self):
        return self.country


class City(models.Model):
    city = models.CharField(max_length = 50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 

    def __str__(self):
        return self.city



class Category(models.Model):
    category = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.category




class Profile(models.Model):

    category = models.ManyToManyField(Category)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null = True) 
    city= models.ForeignKey(City, on_delete=models.CASCADE) 
    location = models.CharField(max_length = 50, null = True, blank=True)
    bio = models.TextField(null = True, blank=True)
    phone_number = models.CharField(max_length=30) 
    profile_pic = models.ImageField(upload_to = 'media/profile/', default='profile/avatar.png')
    website = models.CharField(max_length = 200, null = True, blank=True)
    visite = models.BooleanField(default= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.first_name}, {self.user.last_name}"

    def get_absolute_url(self):
        return reverse('my_profile_page', kwargs={'pk': self.pk})
        
    def profilepic_or_default(self, default_path='profile/default.png'):
        if self.profile_pic:
            return self.profile_pic.url
        return default_path


class Item(models.Model):
    artist = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200, null = True, blank=True)
    image = models.ImageField(upload_to = 'media/items/', default='media/items/default.png')
    description = models.TextField(null = True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    quantity = models.IntegerField(default = 1)


    def itemImage_or_default(self, default_path='media/items/default.png'):
        if self.image:
            return self.image.url
        return default_path

    def sold(self):
        #flat = True to get list of it rather than a tupplelist 
        if self.order_set.filter(completed=True).exists() and self.quantity < 1:
            return True
        else:
            return False
        # thsi function is to automaticaly put it sold (or what ever I want to make it as when ordered) 
    def __str__(self):
        return f"{self.id}, {self.title}"

    def get_absolute_url(self):
        return reverse('view_item', kwargs={'pk': self.pk})


    
# this line is to avoid needing to bring in Order >> creating a circular import  
    # if self.order_set.filter(completed=True).exists() and self.quantity < 1:
        
