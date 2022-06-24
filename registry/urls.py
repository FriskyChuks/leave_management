from django.urls import path
from .import views

urlpatterns = [
    path('employment_detail/<id>/', views.employment_detail_view,name='employment_detail'),
    path('edit_employment_detail/<id>/', views.edit_employment_detail_view,name='edit_employment_detail')
]