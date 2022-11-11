from django.urls import path

from .views import *

urlpatterns = [
    path('active_leave_list/',active_leave_list_view, name='active_leave_list'),
]    