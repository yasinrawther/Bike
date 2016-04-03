from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROLES = (
         ('Admin', 'Admin'),
         ('Vendor', 'Vendor'),
         ('Supervisor', 'Supervisor'),
         ('User', 'User'),
        )

class BikeDetails(models.Model):
    bike_reg_no = models.CharField(max_length=100)
    bike_model = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image', max_length=200)
    km_driven = models.IntegerField(max_length=20)
    top_speed = models.IntegerField(max_length=20)
    milege = models.FloatField(max_length=20)
    fuel_tank_capacity = models.FloatField(max_length=20)
    max_power = models.IntegerField(max_length=20)

class BookingDetails(models.Model):
    user_profile = models.ForeignKey('UserProfile')
    booking_no = models.CharField(max_length=100)
    bike_detail = models.ForeignKey(BikeDetails)
    time_period = models.IntegerField(max_length=20)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=20, default='User', choices=ROLES)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)        
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)

    admin = models.ForeignKey('Admin', null=True, blank=True, related_name='admin_user')
    vendor = models.ForeignKey('Vendors', null=True, blank=True, related_name='vendor_id')
    supervisor = models.ForeignKey('Supervisor', null=True, blank=True, related_name='supervisor_mapping')

class Admin(models.Model):
    user_profile = models.ForeignKey(UserProfile)

class Vendor(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    admin = models.ForeignKey(Admin)

class SuperVisor(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    vendor = models.ForeignKey(Vendor)


    