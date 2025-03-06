from multiprocessing import context
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import models
from django.db.models import Q

from contact.models import *
from registry.models import *
from leave.models import *
from reports.views import total_leave_applications, pending_resumptions, due_resumptions, pending_leave_pass

from .models import User, Gender
from .forms import *
from .decorators import allowed_users


@login_required(login_url='login')
def index(request):
    approval_desk, approval_desk_id, active_app = None, None, None
    excluded = [1, 2, 6, 7]
    status = ['in process', 'partly in process']
    # if request.user.user_group.group == 'head of directorate':
    #     excluded = [1, 6, 7]
    try:
        active_app = LeaveApplication.objects.get(models.Q(
            status__status='active',created_by=request.user) | models.Q(
                status__status='partly active',created_by=request.user))
    except:
        pass
    leave_app = LeaveApplication.objects.filter(
        created_by__id=request.user.id, status__status__in=status)
    for app in leave_app:
        approval_desk = app.approval_status
        approval_desk_id = app.approval_status.id
    approval_status = Approval.objects.all().exclude(id__in=excluded).order_by('-id')
    progress_bar_width = 100/1
    if int(len(approval_status)) > 0:
        progress_bar_width = 100/int(len(approval_status))
    declined_app = LeaveApplication.objects.filter(
        created_by_id=request.user.id).last()
    show_search = request.user.user_group.group in ['support', 'developer', 'leave_and_passage']
    context = {"approval_desk": approval_desk, "approval_desk_id": approval_desk_id,
               "approval_status": approval_status, "progress_bar_width": progress_bar_width,
               "declined_app": declined_app, 'active_app': active_app,'show_search':show_search,
               # calling quick statistics functions
               "total_leave_applications": total_leave_applications,
               "pending_resumptions": pending_resumptions,
               "due_resumptions": due_resumptions,
               'pending_leave_pass': pending_leave_pass, "leave_app": leave_app,
               }
    return render(request, 'home/index.html', context)


def loginPage(request):
    msg, emp_details = None, None
    user_groups = ['head of department', 'head of directorate', 'cmd']
    if request.method == "POST":
        username_var = request.POST.get('username')
        password_var = request.POST.get('password')
        user = authenticate(request, username=username_var,
                            password=password_var)

        qs = User.objects.filter(username=username_var)
        if len(qs) < 1:
            msg = 'This user does not EXIST!'
        try:
            user = User.objects.get(username=username_var)
        except:
            user = None
        if user is not None and not user.check_password(password_var):
            msg = 'Wrong Password'
        elif user is None:
            pass
        else:
            login(request, user)
            if password_var == 'pass':
                messages.info(
                    request, "You're using the default 'password', please change it before you proceed")
                return redirect('change_password')
            if user.user_group.group not in user_groups and user.department.has_unit and not user.unit:
                messages.error(
                    request, "You are not assigned to a Unit, please update that!")
                return redirect('update_user_unit')
            elif "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                try:
                    emp_details = EmploymentDetails.objects.get(
                        user_id=user.id)
                    if not emp_details.grade or not emp_details.ippis_no or not emp_details.designation:
                        messages.info(
                            request, "Please update your record before you continue")
                        return redirect('edit_employment_detail', emp_details.id)
                except ObjectDoesNotExist:
                    return redirect('employment_detail', user.id)
                groups = ['head of unit', 'head of department',
                          'head of directorate', 'cmd']
                if user.user_group.group in groups:
                    return redirect("list_pending_leave_applications")
                else:
                    return redirect("index")

    context = {"msg": msg}
    return render(request, 'accounts/login.html', context)

# logoutUser views


def logoutUser(request):
    logout(request)
    return redirect('login')

# registerUser views


@login_required(login_url='login')
@allowed_users(alllowed_roles=['registry', 'developer', 'support', 'leave_and_passage'])
def registerUser(request):
    gender = Gender.objects.all()
    units = Unit.objects.all()
    depts = Department.objects.all()
    directorates = Directorate.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        other_name = request.POST['other_name']
        file_number = request.POST['file_number']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        directorate = request.POST['directorate']
        department = request.POST['department']
        # unit=request.POST['unit']
        # passport = request.FILES['passport']
        if User.objects.filter(file_number=file_number).exists():
            messages.info(request, 'File Number Already Exists  ')
            return redirect('register')
        else:
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, other_name=other_name, file_number=file_number,
                username=file_number, date_of_birth=date_of_birth, user_group_id=5,
                gender_id=gender, directorate_id=directorate, department_id=department)
            user.set_password("pass")
            user.save()
            return redirect('employment_detail', id=user.id)

    context = {'gender': gender, 'units': units,
               'depts': depts, 'directorates': directorates}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def staff_biodata_summary(request, id):  # id = id
    contact, address, employee = None, None, None
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect("error_handling")
    try:
        contact = Contact.objects.get(user=user)
    except ObjectDoesNotExist:
        pass
    try:
        address = Address.objects.get(user=user)
    except ObjectDoesNotExist:
        pass
    try:
        employee = EmploymentDetails.objects.get(user=user)
    except ObjectDoesNotExist:
        pass
    context = {'user': user, "cont": contact,
               "address": address, "emply": employee}
    return render(request, 'accounts/staff_biodata_summary.html', context)


# updateUser views
@login_required(login_url='login')
def update_view(request, id):
    user = User.objects.get(id=id)
    gender = Gender.objects.all()
    employee_detail = EmploymentDetails.objects.get(user=user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        othernames = request.POST.get('othernames')
        file_number = request.POST.get('file_number')
        sex = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')

        User.objects.filter(id=id).update(first_name=first_name, last_name=last_name, gender_id=sex,
                                          username=file_number, other_name=othernames, file_number=file_number, date_of_birth=date_of_birth)
        return redirect('edit_employment_detail', id=employee_detail.id)

    context = {'user': user, 'gender': gender}
    return render(request, 'accounts/edit_registration.html', context)


def error_handling_view(request):
    return render(request, 'home/page-404.html', {})


def search_unit(request):
    dept = request.GET.get('dept_id')
    units = Unit.objects.filter(department=dept)
    return render(request, 'accounts/units.html', {"units": units})


@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage','support', 'developer'])
def reset_password(request, id):
    user = User.objects.get(id=id)
    user.set_password("pass")
    user.save()
    messages.success(request, "Password reset successful!")
    return redirect('index')


@login_required(login_url='login')
def auto_run_view(request):
    pass
    return redirect('index')


@login_required(login_url='login')
def change_password(request):
    context = {}
    if request.method == "POST":
        new_password = request.POST["new_password"]
        current_password = request.POST["current_password"]
        confirm_password = request.POST["confirm_password"]

        user = User.objects.get(id=request.user.id)
        check = user.check_password(current_password)
        if check == True:
            if new_password != confirm_password:
                context["msg"] = "Password Not Matching "
                context["col"] = "alert-danger"
            else:
                user.set_password(new_password)
                user.save()
                context["msg"] = "Password Change Successfully"
                context["col"] = "alert-success "
                return redirect('logout')
        else:
            context["msg"] = " Current Password is Incorrect "
            context["col"] = "alert-danger"
    return render(request, 'accounts/change_password.html', context)


@login_required(login_url='login')
@allowed_users(alllowed_roles=['support', 'developer', 'head', 'leave_and_passage'])
def search_user(request):
    try:
        query = request.GET.get('q')
    except:
        query = None
    lookups = (Q(file_number__iexact=query) | Q(first_name__icontains=query) |
               Q(last_name__icontains=query) | Q(username__iexact=query))
    if query:
        results = User.objects.filter(lookups).distinct()
        context = {'query': query, "results": results}
        template = 'accounts/search.html'
    else:
        a = "Please enter a search parameter!"
        template = 'accounts/search.html'
        context = {'query1': a}
    return render(request, template, context)


@login_required(login_url='login')
def update_user_unit(request):
    user = User.objects.get(id=request.user.id)
    directorate = Directorate.objects.all().order_by('title')
    units = Unit.objects.filter(
        department_id=user.department.id).order_by('title')
    departments = Department.objects.filter(
        directorate_id=user.directorate.id).order_by('title')
    if request.method == 'POST':
        User.objects.filter(id=request.user.id).update(
            unit_id=request.POST.get('unit'))
        User.objects.filter(id=request.user.id).update(
            department_id=request.POST.get('department'))
        User.objects.filter(id=request.user.id).update(
            directorate_id=request.POST.get('directorate'))
        messages.success(request, "Thanks, your day is blessed!")
        return redirect('index')
    context = {"user": user, "units": units,
               'departments': departments, 'directorates': directorate}
    return render(request, 'accounts/update_user_unit.html', context)


def get_departs(request):
    direct = request.GET.get('direct_id')
    departs = Department.objects.filter(directorate=direct).order_by('title')
    return render(request, 'accounts/departs.html', {"departs": departs})


def get_unit(request):
    dept_id = request.GET.get('dept_id')
    units = Unit.objects.filter(department=dept_id).order_by('title')
    return render(request, 'accounts/unit.html', {"units": units})


@login_required(login_url='login')
@allowed_users(alllowed_roles=['support', 'developer'])
def update_user_group(request, id):
    user = User.objects.get(id=id)
    groups = UserGroup.objects.all().order_by('group')
    if request.method == 'POST':
        User.objects.filter(id=id).update(
            user_group_id=request.POST.get('group'))
        messages.success(request, "Updated Successfully!")
        return redirect('index')
    context = {"user": user, "groups": groups}
    return render(request, 'accounts/update_user_group.html', context)


@login_required(login_url='login')
@allowed_users(alllowed_roles=['support', 'developer'])
def department_list_view(request):
    departments = Department.objects.all().order_by('title')
    return render(request, 'accounts/department_list.html', {'departments': departments})


@login_required(login_url='login')
@allowed_users(alllowed_roles=['support', 'developer'])
def update_department_view(request, id):
    department = Department.objects.get(id=id)
    print(department)
    directorates = Directorate.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        directorate = request.POST.get('directorate')
        has_unit = request.POST.get('has_unit')
        reports_to_cmd = request.POST.get('reports_to_cmd')
        print(reports_to_cmd)
        # if has_unit:
        Department.objects.filter(id=id).update(
            title=title, directorate_id=directorate, has_unit=has_unit, reports_to_cmd=reports_to_cmd)
        messages.success(request, "Updated successfully")

        return redirect('department_list')
    return render(request, 'accounts/update_department.html', {'department': department, 'directorates': directorates})
