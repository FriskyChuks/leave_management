from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','other_name','username','file_number',
            'gender','passport','password1','password2'] #,'nationality'
    

class UpdateUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            ' required':'',
            'name':'first_name',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
    
        self.fields['last_name'].widget.attrs.update({
            ' required':'',
            'name':'last_name',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })

    
       
        self.fields['other_name'].widget.attrs.update({
            ' required':'',
            'name':'other_name',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
    
        self.fields['username'].widget.attrs.update({
            ' required':'',
            'name':'username',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })
    
        self.fields['file_number'].widget.attrs.update({
            ' required':'',
            'name':'file_number',
            'id':'usernameValidate',
            'type':'number',
            'class':"form-control", 
    })
    
        
    #     self.fields['date_of_birth'].widget.attrs.update({
    #         ' required':'',
    #         'name':'date_of_birth',
    #         'id':'usernameValidate',
    #         'type':'date',
    #         'class':"form-control", 
    # })
    
        
        self.fields['gender'].widget.attrs.update({
            ' required':'',
            'name':'gender',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    }) 

    #     self.fields['unit'].widget.attrs.update({
    #         ' required':'',
    #         'name':'unit',
    #         'id':'usernameValidate',
    #         'type':'text',
    #         'class':"form-control", 
    # }) 
   
        self.fields['department'].widget.attrs.update({
            ' required':'',
            'name':'department',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    }) 
   
        self.fields['directorate'].widget.attrs.update({
            ' required':'',
            'name':'directorate',
            'id':'usernameValidate',
            'type':'text',
            'class':"form-control", 
    })     
  
        self.fields['passport'].widget.attrs.update({
            'name':'passport',
            'id':'usernameValidate',
            'type':'file',
            'class':"form-control", 
    })    
    class Meta:
        model = User

        fields = ['first_name','last_name','other_name','username','file_number',
                    'gender','department','directorate','passport'] 
    
    
   