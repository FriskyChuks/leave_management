from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import *
from registry.models import *
from contact.models import *


def leave_type(request):
    form = LeaveTypeForm()
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form} 
    return render(request, 'leave/leavetype.html', context)


def LeaveDurationView(request):
    form = LeaveDurationForm()
    if request.method == 'POST':
        form = LeaveDurationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form':form } 
    return render(request, 'leave/leaveduration.html', context)    


def LeaveApplicationview(request, id):
    # CHECK FOR ACTIVE LEAVE
    excluded = ['Done','Declined']
    active_leave = LeaveApplication.objects.filter(created_by=request.user.id).exclude(
                    status__status__in=excluded)
    if len(active_leave)>=1:
        messages.error(request, "You are not eligible for a leave now; you have an active leave")
        return redirect('index')
    states = State.objects.all()
    leave_type = LeaveType.objects.get(id=id)
    user = request.user
    no_of_days_used = LeaveApplication.objects.filter(
        created_by_id=user,leave_type_id=id).exclude(status__status='Done')   
    # GET TOTAL DAYS USED SO FAR
    duration = 0
    total_days_used = 0
    days_remaining = 0
    for days in no_of_days_used:
        total_days_used += days.requested_duration
    # Get remaining days
    staff = EmploymentDetails.objects.get(user_id=user.id) 
    duration = LeaveDuration.objects.filter(staff_category_id=staff.staff_category.id,leave_type_id=id) | LeaveDuration.objects.filter(staff_category_id=3,leave_type_id=id)
    for duration in duration:            
        days_remaining = duration.duration - total_days_used

    # Get form values
    if request.method =='POST':
        requesting_duration = request.POST.get('requested_duration')
        if days_remaining < int(requesting_duration):
            messages.error(request, f"{leave_type.title} leave duration cannot exceed {duration.duration} days!")
            return redirect('leave_application',id=leave_type.id)
        elif days_remaining <= 0:
            messages.info(request, f"{leave_type.title} leave exhausted!")
            leave_type_id = int(leave_type.id)
            return redirect('leave_application', id=leave_type_id)
        elif int(request.POST.get("requested_duration"))<days_remaining:
            LeaveApplication.objects.create(leave_duration_id=duration.id,created_by_id=user.id,
                                            leave_type_id = leave_type.id,status_id=1,approval_status_id=5,
                                            requested_duration=requesting_duration,
                                            date_from= request.POST.get('date_from'),date_to = request.POST.get('date_to'),
                                            destination_id=request.POST.get('destination'))    
        else:
            LeaveApplication.objects.create(leave_duration_id=duration.id,created_by_id=user.id,
                                            leave_type_id = leave_type.id,status_id=5,approval_status_id=5,
                                            requested_duration=requesting_duration,
                                            date_from= request.POST.get('date_from'),date_to = request.POST.get('date_to'),
                                            destination_id=request.POST.get('destination'))
        return redirect('index')

    context = { 
               "duration":duration,
               "total_days_used":total_days_used,
               "days_remaining":days_remaining,
               "leave_type":leave_type,
               "states":states
            }
    return render(request, 'leave/leave_application.html', context)   


def leave_types_list(request):
    leave_types = LeaveType.objects.all()
    context = {'leave_types':leave_types}
    return render(request, 'leave/leave_types_list.html',context)

def LeaveApplicationStatus(request):
    form = LeaveApplicationStatusForm()
    if request.method == 'POST':
        form =LeaveApplicationStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'leave/leaveapplicationstatus.html', context)    
    
def Leave_list_by_departments(request):
    leave_apps=None
    user = User.objects.get(id=request.user.id) 
    for head in user.head_set.all():
        sub_unit_approval_status = Approval.objects.get(id=6)
        id=sub_unit_approval_status.id
        if head.is_head_of_sub_unit:
            leave_apps = LeaveApplication.objects.filter(approval_status_id=id,created_by__sub_unit__id=request.user.sub_unit.id)
        elif head.is_head_of_unit: 
            leave_apps = LeaveApplication.objects.filter(approval_status_id=id-1,created_by__unit__id=request.user.unit.id)  
        elif head.is_head_of_dept:
            leave_apps = LeaveApplication.objects.filter(approval_status_id=id-2,created_by__department__id=request.user.department.id)
        elif head.is_head_of_directorate:    
             leave_apps = LeaveApplication.objects.filter(approval_status_id=id-3,created_by__directorate__id=request.user.directorate.id)

    context = {'leave_apps': leave_apps}
    return render(request, 'leave/Leave_list_by_departments.html', context)    
 
def recommend_leave_application(request, id):
    leave_application = LeaveApplication.objects.get(id=id)
    current_approval_status = leave_application.approval_status_id
    # UPDATE approva_status LeaveApplications table
    obj = LeaveApplication.objects.filter(id=id).update(approval_status_id=int(current_approval_status)-1)
    # Insert in to Leave_Recommendation
    obj = LeaveRecommendation.objects.create(leave_application_id=leave_application.id,
                                            created_by_id=request.user.id)
    obj.save()
    return redirect('Leave_list_by_departments')

def decline_leave_application(request,id):
    leave_application = LeaveApplication.objects.get(id=id)
    if request.method=='POST':
        obj=LeaveApplication.objects.filter(id=id).update(approval_status_id=1,status_id=7)
        obj= DeclineLeaveApplication.objects.create(leave_application_id=leave_application.id,
                                                    created_by_id=request.user.id)
        obj.save()
        return redirect('Leave_list_by_departments')
    context= {'leave_application':leave_application}
    return render(request, 'leave/decline.html', context)

   
def resume_leave_view(request):
    context = {}
    return render(request, 'leave/leaveresume.html', context)  


def leave_history_view(request):
    leave_applications = LeaveApplication.objects.filter(created_by__id=request.user.id).order_by('-id')
    if request.method == 'POST':
        return redirect('index')
    context = {"leave_applications":leave_applications}
    return render(request, 'leave/leave_history.html', context) 
    

# @login_required(login_url='login')
def leave_details_view(request,id):
    detail = LeaveApplication.objects.get(id=id)
    user = User.objects.get(id=detail.created_by.id)
    emply = EmploymentDetails.objects.get(user=user)
    cont = Contact.objects.get(user=user)
    address = Address.objects.get(user=user)    
    context= {'user':user, 'emply':emply, 'cont':cont, 'address':address, 'detail':detail}
    return render(request, 'leave/leave_details.html', context)
    