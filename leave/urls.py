from unicodedata import name
from django.urls import path
from .import views

urlpatterns = [
    path('leavetype/',views.leave_type, name='leave_type'),
    path('leaveduration/',views.LeaveDurationView , name='leave_duration'),
    path('leaveapplication/<id>/',views.LeaveApplicationview , name='leave_application'),
    path('leaveapplicationstatus/',views.leave_application_status , name='leave_applicationstatus'),
    path('list_pending_leave_applications/',views.list_pending_leave_applications , name='list_pending_leave_applications'),
    # path('leave_resume/',views.resume_leave_view, name='leave_resume'),
    path('leave_types_list/',views.leave_types_list, name='leave_types_list'),
    path('recommend_leave_application/<id>/',views.recommend_leave_application,name='recommend_leave_application'),
    path('decline_leave_application/<id>/',views.decline_leave_application,name='decline_leave_application'),
    path('leave_details/<id>/',views.leave_details_view,name='leave_details'),
    path('leave_history/',views.leave_history_view, name='leave_history'),
    path('leave_status_detail/',views.leave_status_detail, name='leave_status_detail'),
    path('resume_leave/<id>/', views.resume_leave_view, name='resume_leave'),
    path('list_resumption/',views.list_resumption_view,name='list_resumption'),
    path('recommend_resumption_view/<id>/',views.recommend_resumption_view,name='recommend_resumption'),
    path('process_leave_pass/<id>/',views.process_leave_pass_view,name='process_leave_pass'),
    path('acknowledge_leave_resumption/<id>/',views.acknowledge_leave_resumption_view,name='acknowledge_leave_resumption'),
    path('list_declined_applications/',views.list_declined_applications_view,name='list_declined_applications'),
    path('user_approved_application_list/',views.user_approved_application_list,name='user_approved_application_list'),
    path('pdf_view/<id>/',views.render_pdf_view,name='pdf_view'),
    path('approved_leave/',views.approved_leave_appcation_list,name='approved_leave'),
    path('create_department', views.create_department,name='create_department'),
    path('create_unit',views.create_unit, name='create_unit'),
    path('leave_tracker/<id>/',views.leave_tracker_view,name='leave_tracker'),
    path('update_leave_application/<id>/',views.update_leave_application,name='update_leave_application'),
]    