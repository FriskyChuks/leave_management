from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import *

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        # fields = '__all__'
        exclude = ['user'] 


class AddressForm(ModelForm):
    class Meta:
        model = Address
        # fields = '__all__' 
        exclude = ['user']       