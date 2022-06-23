from django.urls import path
from .import views

urlpatterns = [
    path('leavetype/',views.leave_type, name='leave_type'),
    path('leaveduration/',views.LeaveDurationView , name='leave_duration'),
    path('leaveapplication/<id>/',views.LeaveApplicationview , name='leave_application'),
    path('leaveapplicationstatus/',views.LeaveApplicationStatus , name='leave_applicationstatus'),
    path('Leave_list_by_departments/',views.Leave_list_by_departments , name='Leave_list_by_departments'),
    path('leave_resume/',views.resume_leave_view, name='leave_resume'),
    path('leave_types_list/',views.leave_types_list, name='leave_types_list'),
    path('recommend_leave_application/<id>/',views.recommend_leave_application,name='recommend_leave_application'),
    path('decline_leave_application/<id>/',views.decline_leave_application,name='decline_leave_application'),
    path('leave_details/<id>/',views.leave_details_view,name='leave_details'),
    path('leave_history/',views.leave_history_view, name='leave_history'),

]    