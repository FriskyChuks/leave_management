from django.urls import path
from .import views

urlpatterns = [
    path('<id>/', views.employment_detail_view,name='employment_detail')
]