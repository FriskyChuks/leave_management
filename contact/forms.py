from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['user'] 
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['local_government_area'].queryset=LocalGovernmentArea.objects.none()

        if 'state_of_origin' in self.data:
            try:
                state_id = int(self.data.get('state_of_origin'))
                self.fields['local_government_area'].queryset =LocalGovernmentArea.objects.filter(state_id=state_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['local_government_area'].queryset= self.instance.state_of_origin.local_government_area_set.order_by('title')


class AddressForm(forms.ModelForm):  
    class Meta:
        model = Address
        # fields = '__all__' 
        exclude = ['user'] 

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['local_government_area_of_residence'].queryset=LocalGovernmentArea.objects.none()
        self.fields['local_government_area_of_permanent'].queryset=LocalGovernmentArea.objects.none()

        if 'state_of_residence' in self.data:
            try:
                state_id = int(self.data.get('state_of_residence'))
                self.fields['local_government_area_of_residence'].queryset =LocalGovernmentArea.objects.filter(state_id=state_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['local_government_area_of_residence'].queryset= self.instance.residential_address.local_government_area_of_residence_set.order_by('title') 

        if 'state_of_permanent' in self.data:
            try:
                state_id = int(self.data.get('state_of_permanent'))
                self.fields['local_government_area_of_permanent'].queryset =LocalGovernmentArea.objects.filter(state_id=state_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['local_government_area_of_permanent'].queryset= self.instance.state_of_permanent.local_government_area_of_permanent_set.order_by('title') 


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
        self.fields['phone2'].widget.attrs.update({
            ' required':'',
            'name':'phone2',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
        self.fields['phone1'].widget.attrs.update({
            ' required':'',
            'name':'phone1',
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
            
            'type':'text',
            'class':"form-control", 
    })
        self.fields['local_government_area_of_residence'].widget.attrs.update({
            ' required':'',
            'name':'local_government_area_of_residence',
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