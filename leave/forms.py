from django.forms import ModelForm
from .models import *
from django.forms.widgets import DateInput


class LeaveTypeForm(ModelForm):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveDurationForm(ModelForm):
    class Meta:
        model = LeaveDuration
        fields = '__all__'


class LeaveApplicationForm(ModelForm):
    class Meta:
        model = LeaveApplication
        # fields = '__all__'
        exclude = ['leave_duration','created_by','status','leave_type']
        widgets ={
            'date_from': DateInput(attrs={'type': 'date'}), 'date_to': DateInput(attrs={'type': 'date'}),
            'date_created': DateInput(attrs={'type': 'date'}), 

        }
        

class LeaveApplicationStatusForm(ModelForm):
    class Meta:
        model = LeaveApplicationStatus
        fields = '__all__' 