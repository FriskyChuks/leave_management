from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import models
import datetime
from django.utils import timezone

from contact.models import *
from registry.models import *
from leave.models import *

from .models import User,Gender
from .forms import *
from .decorators import allowed_users

def total_leave_applications():
	now = timezone.now()
	total_applications = LeaveApplication.objects.aggregate(
        total=models.Count('id'),
        today=models.Count('id', filter=models.Q(date_created__date=now.date())),
        # yesterday=models.Count('id', filter=models.Q(date_created__date__gte=(
		# 			now - datetime.timedelta(hours=24)).date())),
        last_7_day=models.Count('id', filter=models.Q(date_created__date__gt=(
					now - datetime.timedelta(days=7)).date())),
    )
	return total_applications

def pending_applications():
	now = timezone.now()
	_status=['in process', 'partly in process']
	pending_applications = LeaveApplication.objects.aggregate(
        total=models.Count('id'),
        today=models.Count('id', filter=models.Q(status__status__in=_status,
										date_created__date=now.date())),
        # yesterday=models.Count('id', filter=models.Q(status__status__in=_status,
		# 			date_created__date__gte=(now - datetime.timedelta(hours=24)).date())),
        last_7_day=models.Count('id', filter=models.Q(status__status__in=_status,
						date_created__date__gt=(now - datetime.timedelta(days=7)).date())),
    )
	return pending_applications

def pending_resumptions():
	now = timezone.now()
	_status=['in process', 'partly in process']
	pending_resumptions = LeaveApplication.objects.aggregate(
        total=models.Count('id'),
        today=models.Count('id', filter=models.Q(resumption_approval__approval='none',
										last_updated__date=now.date())),
        # yesterday=models.Count('id', filter=models.Q(resumption_approval__approval='none',
		# 			last_updated__date__gte=(now - datetime.timedelta(hours=24)).date())),
        last_7_day=models.Count('id', filter=models.Q(resumption_approval__approval='none',
						last_updated__date__gt=(now - datetime.timedelta(days=7)).date())),
    )
	return pending_resumptions


def due_resumptions():
	now = timezone.now()
	due_resumptions = LeaveApplication.objects.aggregate(
        # total=models.Count('id'),
        today=models.Count('id', filter=models.Q(date_to=now.date())),
        overdue=models.Count('id', filter=models.Q(date_to__lt=now.date()))
    )
	return due_resumptions


# Create your views here.
@login_required(login_url='login')
def index(request):
	approval_desk,approval_desk_id=None,None
	excluded = [1]
	status=['in process','partly in process']
	leave_app = LeaveApplication.objects.filter(created_by__id=request.user.id, status__status__in=status)
	for app in leave_app:
		approval_desk = app.approval_status
		approval_desk_id = app.approval_status.id
	approval_status = Approval.objects.all().exclude(id__in=excluded).order_by('-id')
	progress_bar_width=100/int(len(approval_status))
	
	context={"approval_desk":approval_desk, "approval_desk_id":approval_desk_id,
			"approval_status":approval_status,"progress_bar_width":progress_bar_width,
			# calling quick statistics functions
			"total_leave_applications":total_leave_applications,
			"pending_resumptions":pending_resumptions,
			"due_resumptions":due_resumptions,
			'pending_applications':pending_applications,
		}
	return render(request, 'home/index.html',context)


def loginPage(request):
	msg=None
	userlogin = request.user
	# print(userlogin.id)
	if request.method == "POST":
		username_var = request.POST.get('username')
		password_var = request.POST.get('password')
		user = authenticate(request,username=username_var, password=password_var)

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
			# messages.success(request, "Welcome" + " " + str(userlogin))
			if "next" in request.POST:
				return redirect(request.POST.get('next'))
			else:
				if Head.objects.filter(user_id=request.user.id).exists():
					return HttpResponseRedirect("Leave_list_by_departments")
				else:
					return redirect("index")

	context = {"msg":msg}
	return render(request, 'accounts/login.html', context)

#logoutUser views
def logoutUser(request):
	logout(request)
	return redirect('login')

#registerUser views
@login_required(login_url='login')
@allowed_users(alllowed_roles=['registry','developer'])
def registerUser(request):
	gend = Gender.objects.all()
	unit = Unit.objects.all()
	dept = Department.objects.all()
	direct = Directorate.objects.all()
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		other_name = request.POST['other_name']
		file_number = request.POST['file_number']
		username = request.POST['username']
		date_of_birth = request.POST['date_of_birth']
		gender = request.POST['gender']
		directorate = request.POST['directorate']
		department = request.POST['department']
		unit=request.POST['unit']
		passport = request.FILES['passport']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
	
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username Already Exists')
				return HttpResponseRedirect('register')

			elif User.objects.filter(file_number=file_number).exists():
				messages.info(request, 'File Number Already Exists  ') 
				return redirect('register')  
			else:
				user = User.objects.create_user(
					first_name=first_name,last_name=last_name,other_name=other_name,file_number=file_number,
					username=username,date_of_birth=date_of_birth,passport=passport,password=password1,
					gender_id=gender,directorate_id=directorate,department_id=department,unit_id=unit)
				user.save();
				return redirect('employment_detail',id=user.id)
		else:
			messages.info(request, "Password Not Matching")
			return redirect('register')
	context = {'gend':gend,'unit':unit,'dept':dept,'direct':direct}                 
	return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def staff_biodata_summary(request,id):# id = id
	try:
		user = User.objects.get(id=id)
	except ObjectDoesNotExist:
		return redirect("error_handling")
	contact = Contact.objects.get(user=user)
	address = Address.objects.get(user=user)
	employee = EmploymentDetails.objects.get(user=user)
	context= {'user':user,"cont":contact,"address":address,"emply":employee}
	return render(request, 'accounts/staff_biodata_summary.html', context )


#updateUser views
@login_required(login_url='login')
def update_view(request ,id):
    user = User.objects.get(id=id)
    form = UpdateUserForm(instance=user)

    employee_detail = EmploymentDetails.objects.get(user=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save(commit=False)
            form.user_id = id
            form.save()
            return redirect('edit_employment_detail',id=employee_detail.id)
    context =  {'form': form, 'user':user}
    return render(request, 'accounts/edit_registration.html',context)

def error_handling_view(request):
	return render(request, 'home/page-404.html',{})
	

