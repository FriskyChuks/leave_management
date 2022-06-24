from django.urls import path
from .import views


urlpatterns = [
    path('contact_address/<id>/',views.contact_address_views, name='contact_address'),
    path('edit_contact_address/<id>/',views.edit_contact_address_views, name='edit_contact_address'),
]         
