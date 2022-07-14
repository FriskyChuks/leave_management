from django.forms import ModelForm

from .models import *


class edit_Employment_DetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ministry'].widget.attrs.update({
            ' required':'',
            'name':'ministry',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
    
        self.fields['designation'].widget.attrs.update({
            ' required':'',
            'name':'designation',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })  
        self.fields['salary_scale'].widget.attrs.update({
            ' required':'',
            'name':'salary_scale',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
    
        self.fields['grade'].widget.attrs.update({
            ' required':'',
            'name':'grade',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
    
        
        self.fields['step'].widget.attrs.update({
            ' required':'',
            'name':'step',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
    
        
        self.fields['ippis_no'].widget.attrs.update({
            ' required':'',
            'name':'ippis_no',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    }) 

    class Meta:
        model = EmploymentDetails

        exclude = ['user','staff_category'] 