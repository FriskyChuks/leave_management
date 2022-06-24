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


class UpdateContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            ' required':'',
            'name':'email',
            'id':'usernameValidate',
            'type':'email',
            'class':"form-control", 
    })
        self.fields['phone_no'].widget.attrs.update({
            ' required':'',
            'name':'phone_no',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
        self.fields['mobile_no'].widget.attrs.update({
            ' required':'',
            'name':'mobile_no',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
        self.fields['nationality'].widget.attrs.update({
            ' required':'',
            'name':'nationality',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['state_of_origin'].widget.attrs.update({
            ' required':'',
            'name':'state_of_origin',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['local_government_area'].widget.attrs.update({
            ' required':'',
            'name':'local_government_area',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['next_of_kin'].widget.attrs.update({
            ' required':'',
            'name':'next_of_kin',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['next_of_kin_phone_no'].widget.attrs.update({
            ' required':'',
            'name':'next_of_kin_phone_no',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
        self.fields['address_of_next_of_kin'].widget.attrs.update({
            ' required':'',
            'name':'address_of_next_of_kin',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })

    
    class Meta:
        model = Contact
        exclude = ['user'] 


class UpdateAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['residential_address'].widget.attrs.update({
            ' required':'',
            'name':'residential_address',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['state_of_residence'].widget.attrs.update({
            ' required':'',
            'name':'state_of_residence',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['local_government_area_of_residence'].widget.attrs.update({
            ' required':'',
            'name':'local_government_area_of_residence',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['permanent_home_address'].widget.attrs.update({
            ' required':'',
            'name':'permanent_home_address',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['state_of_permanent'].widget.attrs.update({
            ' required':'',
            'name':'state_of_permanent',
            'type':'text',
            'class':"form-control", 
    })
        self.fields['local_government_area_of_permanent'].widget.attrs.update({
            ' required':'',
            'name':'local_government_area_of_permanent',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
     
    class Meta:
        model = Address
        exclude = ['user']     