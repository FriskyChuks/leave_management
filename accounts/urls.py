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
    path('reset_password/<int:id>/', views.reset_password, name='reset_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('search_unit/', views.search_unit, name='search_unit'),
    path('search/',views.search_user,name='search'),
    path('update_user_unit/',views.update_user_unit, name='update_user_unit'),
    path('update_user_group/<id>/',views.update_user_group,name='update_user_group'),
    path('get_unit/',views.get_unit,name='get_unit'),
    path('get_departs/',views.get_departs,name='get_departs'),
    path('department_list/',views.department_list_view,name='department_list'),
    path('update_department/<id>/',views.update_department_view,name='update_department'),
    path('update_db_by_excel_file/', views.update_db_by_excel_file, name='update_db_by_excel_file'),
]

