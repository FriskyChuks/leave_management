from django.db import models
from accounts.models import *

# Create your models here.
class Continent(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title 

class Country(models.Model):
    title = models.CharField(max_length=50)
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class State(models.Model):
    title = models.CharField(max_length=50)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class LocalGovernmentArea(models.Model):
    title = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    nationality =models.ForeignKey(Country, on_delete=models.CASCADE,null=True,blank=True)
    state_of_origin = models.ForeignKey(State, on_delete=models.CASCADE, null=True,blank=True)
    local_government_area = models.ForeignKey(LocalGovernmentArea, on_delete=models.CASCADE, null=True,blank=True)
    next_of_kin = models.CharField(max_length=50)
    next_of_kin_phone_no = models.CharField(max_length=150)
    address_of_next_of_kin = models.CharField(max_length=150)
    

    def __str__(self):
        return str(self.user)

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    residential_address = models.CharField(max_length=100)
    state_of_residence = models.ForeignKey(State, on_delete=models.CASCADE)
    local_government_area_of_residence = models.ForeignKey(LocalGovernmentArea, on_delete=models.CASCADE, null=True,blank=True)
    permanent_home_address = models.CharField(max_length=100)
    state_of_permanent = models.ForeignKey(State, related_name='states', on_delete=models.CASCADE)
    local_government_area_of_permanent = models.ForeignKey(LocalGovernmentArea, related_name='lga', on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return str(self.residential_address)