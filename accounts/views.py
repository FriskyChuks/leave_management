from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

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
		last_7_day=models.Count('id', filter=models.Q(date_created__date__gt=(
					now - timedelta(days=7)).date())),
	)
	return total_applications

def pending_leave_pass():
	now = timezone.now()
	pending_leave_pass = LeaveApplication.objects.aggregate(
		total=models.Count('id'),
		today=models.Count('id', filter=models.Q(approval_status__approval='cmd',
										last_updated__date__gte=now.date())),
		# yesterday=models.Count('id', filter=models.Q(status__status__in=_status,
		# 			date_created__date__gte=(now - datetime.timedelta(hours=24)).date())),
		last_7_day=models.Count('id', filter=models.Q(approval_status__approval='cmd',
						last_updated__date__gt=(now - timedelta(days=7)).date())),
	)
	return pending_leave_pass

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
						last_updated__date__gt=(now - timedelta(days=7)).date())),
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
	excluded = [1,2,6,7]
	status=['in process','partly in process']
	leave_app = LeaveApplication.objects.filter(created_by__id=request.user.id, status__status__in=status)
	for app in leave_app:
		approval_desk = app.approval_status
		approval_desk_id = app.approval_status.id
	approval_status = Approval.objects.all().exclude(id__in=excluded).order_by('-id')
	progress_bar_width=100/1
	if int(len(approval_status)) > 0:
		progress_bar_width=100/int(len(approval_status))
	declined_app = LeaveApplication.objects.filter(created_by_id=request.user.id).last()
	
	context={"approval_desk":approval_desk, "approval_desk_id":approval_desk_id,
			"approval_status":approval_status,"progress_bar_width":progress_bar_width,
			"declined_app":declined_app,
			# calling quick statistics functions
			"total_leave_applications":total_leave_applications,
			"pending_resumptions":pending_resumptions,
			"due_resumptions":due_resumptions,
			'pending_leave_pass':pending_leave_pass,
		}
	return render(request, 'home/index.html',context)


def loginPage(request):
	msg,emp_details=None,None
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
			if user.department.has_unit and not user.unit:
				messages.info(request,"You are not assigned to a Unit, please update that!")
				return redirect('update_user_unit')
			elif "next" in request.POST:
				return redirect(request.POST.get('next'))
			else:
				try:
					emp_details=EmploymentDetails.objects.get(user_id=user.id)
					if not emp_details.grade or not emp_details.ippis_no or not emp_details.designation:
						messages.info(request,"Please update your record before you continue")
						return redirect('edit_employment_detail',emp_details.id)
				except ObjectDoesNotExist:
					return redirect('employment_detail',user.id)
				if Head.objects.filter(user_id=request.user.id).exists():
					return HttpResponseRedirect("list_pending_leave_applications")
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
	gender = Gender.objects.all()
	units = Unit.objects.all()
	depts = Department.objects.all()
	directorates = Directorate.objects.all()
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
		# unit=request.POST['unit']
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
					gender_id=gender,directorate_id=directorate,department_id=department)
				user.save();
				return redirect('employment_detail',id=user.id)
		else:
			messages.info(request, "Password Not Matching")
			return redirect('register')
	context = {'gender':gender,'units':units,'depts':depts,'directorates':directorates}                 
	return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def staff_biodata_summary(request,id):# id = id
	contact,address,employee=None,None,None
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

def search_unit(request):
	dept = request.GET.get('dept_id')
	units =Unit.objects.filter(department=dept)
	return render(request,'accounts/units.html',{"units":units})


@login_required(login_url='login')
def reset_password(request,id):
	user = User.objects.get(id=id)
	user.set_password("password")
	user.save()
	messages.success(request, "Password reset successful!")
	return redirect('index')
	
	 	
@login_required(login_url='login')
def auto_run_view(request):
	pass
	# users=User.objects.filter(password='')
	# for user in users:
	# 	user.set_password('pass')
	# 	user.save()

	# users=User.objects.all()
	# ippis_no=None
	# for user in users:
	# 	if user.ippis_no:
	# 		ippis_no=user.ippis_no
	# 	emp_detail=EmploymentDetails.objects.get_or_create(
	# 		user_id=user.id,
	# 		ministry='Health',
	# 		salary_scale_id=user.salary_scale.id,
	# 		grade_id=user.grade_level.id,
	# 		ippis_no=ippis_no
	# 	)

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
		else:
			context["msg"] = " Current Password is Incorrect "
			context["col"] = "alert-danger"	
	return render(request, 'accounts/change_password.html',context)


def assign_heads_view(request,id):
	groups = UserGroup.objects.all()
	user=User.objects.get(id=id)
	
	sub_unit =bool(request.POST.get('sub_unit'))
	unit = bool(request.POST.get('unit'))
	department = bool(request.POST.get('department'))
	directorate = bool(request.POST.get('directorate'))
	# group=request.POST.get('group')	
	group_id = UserGroup.objects.get(group='head').id
	user_is_head = Head.objects.filter(user_id=id)

	if request.method=="POST":
		if user_is_head:
			Head.objects.filter(user_id=id).update(user_id=id,is_head_of_unit=unit,
			is_head_of_dept=department,is_head_of_directorate=directorate)
		else:
			Head.objects.create(user_id=id,is_head_of_unit=unit,
			is_head_of_dept=department,is_head_of_directorate=directorate)
		User.objects.filter(id=id).update(user_group_id=group_id)
		messages.success(request,"Successfully assigned!")
		return redirect('index')
	context={"groups":groups,"user":user}
	return render(request,'accounts/assign_heads.html',context)


def search_user(request):
	try:
		query = request.GET.get('q')
	except:
		query = None
	lookups = ( Q(file_number__iexact=query) | Q(first_name__icontains=query)| 
				Q(last_name__icontains=query) | Q(username__iexact=query))
	if query:
		results = User.objects.filter(lookups).distinct()
		context = {'query': query,"results":results}
		template = 'accounts/search.html'
	else:
		a = "Please enter a search parameter!"
		template = 'accounts/search.html'
		context = {'query1': a}
	return render(request, template, context)


def update_user_unit(request):
	user=User.objects.get(id=request.user.id)
	units=Unit.objects.filter(department_id=user.department.id).order_by('title')
	if request.method=='POST':
		User.objects.filter(id=request.user.id).update(unit_id=request.POST.get('unit'))
		messages.success(request,"Thanks for being positive today!")
		return redirect('index')
	context={"user":user,"units":units}
	return render(request,'accounts/update_user_unit.html',context)

def update_user_group(request,id):
	user=User.objects.get(id=id)
	groups=UserGroup.objects.all()
	if request.method=='POST':
		User.objects.filter(id=id).update(user_group_id=request.POST.get('group'))
		messages.success(request,"Updated Successfully!")
		return redirect('index')
	context={"user":user,"groups":groups}
	return render(request,'accounts/update_user_group.html',context)