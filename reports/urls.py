from django.urls import path

from .views import *

urlpatterns = [
    path('active_leave_list/',active_leave_list_view, name='active_leave_list'),
    path('general_leave_report/',general_leave_report,name='general_leave_report'),
]    