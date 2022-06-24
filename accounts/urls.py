from django.urls import path
from .import views

urlpatterns = [
    path('',views.loginPage, name='login'),
    path('index/',views.index, name='index'),
    path('register/',views.registerUser, name='register'),
    path('logout/',views.logoutUser, name='logout'),
    path('update/<id>/',views.update_view, name= 'update'),
    path('staff_biodata/<id>/', views.staff_biodata_summary, name='staff_biodata'),
    path('error_handling/', views.error_handling_view, name='error_handling'),
]

