from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self,postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['pw_confirm']:
            errors['password'] = "Passwords do not match"
        same_email = User.objects.filter(email = postData['email'])
        if len(same_email) > 0:
            errors['email'] = "Email already exists"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Park(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255) #northern, southern, coast
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Campsite(models.Model):
    name = models.CharField(max_length=255)
    season_open = models.DateField() #day it opens
    season_closed = models.DateField()
    status = models.CharField(max_length=45)
    water = models.CharField(max_length=255) #status of water at campsite
    number_sites = models.IntegerField()
    nightly_rate = models.DecimalField(decimal_places=2, max_digits=5)
    elevation = models.IntegerField()
    park = models.ForeignKey(Park, related_name="campsites") #park this campsite belongs to
    favorites = models.ManyToManyField(User, related_name="favorited_campsites") #users can add to favorites
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Booking(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    nights = models.IntegerField()
    site_number = models.IntegerField()
    site_loop = models.CharField(max_length=2)
    phone_number = models.IntegerField()
    occupants = models.IntegerField()
    vehicles = models.IntegerField()
    site_type = models.CharField(max_length=15) #tent, rv, trailer
    total_price = models.DecimalField(decimal_places=2, max_digits=6)
    user = models.ManyToManyField(User, related_name="bookings")
    campsite = models.ForeignKey(Campsite, related_name="site_bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

