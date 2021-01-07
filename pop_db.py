import django
# os to interact with computer
import os
from faker import Faker
import random
# setting the env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artizen.settings')
# this line will check for the setting to know where to save it
django.setup()
# after the above step >> we can import models
from artists.models import Country, City, Profile, Category
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd

import json
import urllib
import requests


# here we sep the csv file with the sep as if I cehck the data with data.key() see what data Im dealing with so i see what I get, then to know how to reach it.

def get_country_data():
    data = pd.read_csv('countries.csv', sep = '\t')
    countries = data['name']
    return countries


def get_or_create(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return model.objects.create(**kwargs)



def pop_country():
    country = get_country_data()
    for name in country:
        Country.objects.get_or_create(country=name)

    print(f"{len(country)} countries were added to your DB ")



# ----pop cities

def get_cities_data():
    data = pd.read_csv('worldcities.csv', usecols=['city', 'country'])
    return data


# def pop_cities():
#     city_list = get_cities_data()
#     for city, country in zip(city_list['city'], city_list['country']):
#         country_obj, created = Country.objects.get_or_create(country= country)
#         City.objects.get_or_create(city=city, country =country_obj)

#     print(f"{len(city_list)} countries were added to your DB ")



# -----pop city -BULK!!!

def pop_cities():
    city_list = get_cities_data()
    cities =[]
    for city, country in zip(city_list['city'], city_list['country']):

        country_obj, created = Country.objects.get_or_create(country= country)

        cities.append(City(city=city, country =country_obj))

    City.objects.bulk_create(cities)   #this si save at this point only to db
    print(f"{len(city_list)} countries were added to your DB ")



category_list = ['Paint', 'Sculpture', 'Food', 'Home&Stuff', 'Fashion', 'Other']

def pop_category(category_list):
    for cat in category_list:
        cat = Category.objects.create(category=cat)
    
        print(f"the category {cat} was created")



# pop_cities()

fak = Faker()


def pop_users(n):
    for i in range(n):
        user = User.objects.create_user(
            first_name = fak.first_name(),
            last_name =fak.last_name(),
            email = fak.email(),
            username =  fak.user_name(),
            password = '123456')



        profile = Profile.objects.create(
            city= random.choice(City.objects.all()),
            location = '',
            bio = "This is about me ....",
            profile_pic = 'media/profile/avatar.png',
            website = 'www.google.com',  
               
            user = user,       
            )
        profile.category.add(random.choice(Category.objects.all()))

        print(f'Created Profile:{profile.id}')

    # finished
    print(f"Finished...{n} entries populated.")


pop_users(30)