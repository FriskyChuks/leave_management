from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','other_name','username','file_number','date_of_birth','gender','passport','password1','password2'] #,'nationality'
    

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','other_name','username','first_name','last_name','other_name','date_of_birth','gender','passport'] #,'nationality'
    
   