from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# for pdf print
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

from accounts.decorators import allowed_users
from .logics import *
from .models import *
from .forms import *
from registry.models import *
from contact.models import *


@login_required(login_url='login')
@allowed_users(alllowed_roles=['support','developer'])
def leave_type(request):
	form = LeaveTypeForm()
	if request.method == 'POST':
		form = LeaveTypeForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.created_by_id = request.user.id
			obj.save()
			return redirect('leave_type')
	context = {'form':form} 
	return render(request, 'leave/leavetype.html', context)

@login_required(login_url='login')
@allowed_users(alllowed_roles=['support','developer'])
def LeaveDurationView(request):
	form = LeaveDurationForm()
	if request.method == 'POST':
		form = LeaveDurationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')
	context = {'form':form } 
	return render(request, 'leave/leaveduration.html', context)


@login_required(login_url='login')
def LeaveApplicationview(request, id): 
	user_groups = ['head of department','head of directorate']
	try:
		emp_details=EmploymentDetails.objects.get(user_id=request.user.id)
		if not emp_details.grade or not emp_details.designation or not emp_details.step:
			messages.info(request,"Please update your record before you continue")
			return redirect('edit_employment_detail',emp_details.id)
	except ObjectDoesNotExist:
		return redirect('employment_detail',request.user.id)
	# CHECK IF USER HAS A UNIT 
	if request.user.user_group.group not in user_groups and request.user.department.has_unit and not request.user.unit:
				messages.info(request,"You are not assigned to a Unit, please update that before you continue!")
				return redirect('update_user_unit')  
	# check for active leave 
	if len(check_for_active_leave(request))>=1:
		messages.error(request, "You are not eligible for a leave now; you have an active leave")
		return redirect('index')    
	states = State.objects.all()
	leave_type = LeaveType.objects.get(id=id)
	
	user = request.user
	this_year = datetime.now()
	approval_status=Approval.objects.get(approval='declined')
	no_of_days_used = LeaveApplication.objects.filter(
		created_by_id=user.id,leave_type_id=id,date_from__year=this_year.year).exclude(approval_status=approval_status)
	duration,total_days_used,days_remaining = 0,0,0
	for days in no_of_days_used:
		total_days_used += days.requested_duration
	# Get remaining days
	staff = EmploymentDetails.objects.get(user_id=user.id) 
	duration = LeaveDuration.objects.filter(staff_category_id=staff.staff_category.id,leave_type_id=id) |\
				 LeaveDuration.objects.filter(staff_category_id=3,leave_type_id=id)
	for duration in duration:            
		days_remaining = duration.duration - total_days_used

	# CHECK IF USER IS --unit_head, dept_head or directorate_head
	approval_status=check_if_user_is_head(request)
	# Get form values
	if request.method =='POST': 
		if check_current_year(request,leave_type.id):
			messages.error(request,f"You cannot take {leave_type.title} leave twice\
								 in same year; You may re-apply next year, thanks")
			return redirect('index')
		# Check if last leave is atleast 6 months ago
		last_leave = check_leave_eligibility(request,leave_type.id)
		if last_leave < 6:
			messages.error(request,f"Your last Annual leave is only {last_leave} months ago;\
						You may re-apply in {6-last_leave} months, thanks")
			return redirect('index')
		date_from = request.POST.get('date_from')
		date_to = request.POST.get('date_to') 

		requesting_duration = request.POST.get('requested_duration')
		# CHECK MATERNITY LEAVE FOR USED ANNUAL LEAVE
		if leave_type.title.lower() == "maternity" and has_annual_leave(request.user.id):
			requesting_duration=int(requesting_duration)-int(has_annual_leave(request.user.id))
			date_to=datetime.strptime(date_to, '%Y-%m-%d')
			date_to -= timedelta(days=int(has_annual_leave(request.user.id)))
			date_to=date_to.date()
			messages.info(request, f"The days used for Annual leave has been deducted upfront \
				You now have {requesting_duration}days left for your Maternity leave; Thanks!")
			# ENDS HERE
		if days_remaining < int(requesting_duration):
			messages.error(request, f"{leave_type.title} leave duration cannot exceed {duration.duration} days!")
			return redirect('leave_application',id=leave_type.id)
		elif days_remaining <= 0:
			messages.info(request, f"{leave_type.title} leave exhausted!")
			leave_type_id = int(leave_type.id)
			return redirect('leave_application', id=leave_type_id)

		elif int(request.POST.get("requested_duration"))<days_remaining:
			LeaveApplication.objects.create(leave_duration_id=duration.id,created_by_id=user.id,
			leave_type_id = leave_type.id,status_id=1,approval_status_id=approval_status,
			requested_duration=requesting_duration,destination_id=request.POST.get('destination'),
			date_from=date_from, date_to=date_to)    
		else:
			LeaveApplication.objects.create(leave_duration_id=duration.id,created_by_id=user.id,
			leave_type_id = leave_type.id,status_id=5,approval_status_id=approval_status,
			requested_duration=requesting_duration,destination_id=request.POST.get('destination'),
			date_from=date_from, date_to=date_to)
		return redirect('index')

	context = {"duration":duration,"total_days_used":total_days_used,"states":states,
			   "days_remaining":days_remaining,"leave_type":leave_type,}
	return render(request, 'leave/leave_application.html', context)   


def leave_types_list(request):
	leave_types = LeaveType.objects.all()
	context = {'leave_types':leave_types}
	return render(request, 'leave/leave_types_list.html',context)


@login_required(login_url='login')
def leave_application_status(request):
	form = LeaveApplicationStatusForm()
	if request.method == 'POST':
		form =LeaveApplicationStatusForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')
	context = {'form': form}
	return render(request, 'leave/leaveapplicationstatus.html', context)    


@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage','head of unit','head of department','head of directorate','developer','support'])	
def list_pending_leave_applications(request):
	leave_apps=None
	user = User.objects.get(id=request.user.id) 
	groups=['head of unit','head of department','head of directorate']
	heads = User.objects.filter(id=request.user.id,user_group__group__in=groups)
	sub_unit_approval_status = Approval.objects.get(approval='head of sub-unit') # for id=6
	id=sub_unit_approval_status.id
	excluded_status=['done','partly done']
	# for leave & passage staff
	if request.user.user_group.group=='leave_and_passage':
		leave_apps = LeaveApplication.objects.filter(approval_status_id=id-4).exclude(status_id=8)
	else:
		for user in heads:
			if user.user_group.group == 'head of unit': 
				leave_apps = LeaveApplication.objects.filter(approval_status_id=id-1,
									created_by__unit__id=request.user.unit.id).exclude(status__status=excluded_status) 
			elif user.user_group.group == 'head of department':
				leave_apps = LeaveApplication.objects.filter(approval_status_id=id-2,
						created_by__department__id=request.user.department.id).exclude(status__status=excluded_status)
			elif user.user_group.group == 'head of directorate':    
					leave_apps = LeaveApplication.objects.filter(approval_status_id=id-3,
						).exclude(status__status=excluded_status)

	context = {'leave_apps': leave_apps}
	return render(request, 'leave/list_pending_leave_applications.html', context)    


@login_required(login_url='login')
@allowed_users(alllowed_roles=['head of unit','head of department','head of directorate'])
def recommend_leave_application(request, id):
	leave_application = LeaveApplication.objects.get(id=id)
	current_approval_status = leave_application.approval_status_id
	# UPDATE approval_status LeaveApplications table
	obj = LeaveApplication.objects.filter(id=id).update(approval_status_id=int(current_approval_status)-1)
	# Insert in to Leave_Recommendation
	obj = LeaveRecommendation.objects.create(leave_application_id=leave_application.id,
											created_by_id=request.user.id)
	obj.save()
	return redirect('list_pending_leave_applications')


@login_required(login_url='login')
@allowed_users(alllowed_roles=['head of unit','head of department','head of directorate'])
def decline_leave_application(request,id):
	leave_application = LeaveApplication.objects.get(id=id)
	_status = LeaveApplicationStatus.objects.get(status='declined')
	approval_status=Approval.objects.get(approval='declined')
	if request.method=='POST':
		comment=request.POST.get('comment')
		obj=LeaveApplication.objects.filter(id=id).update(
								approval_status_id=approval_status,status_id=_status)
		obj= DeclineLeaveApplication.objects.create(leave_application_id=leave_application.id,
					comment=comment,created_by_id=request.user.id)
		obj.save()
		return redirect('list_pending_leave_applications')
	context= {'leave_application':leave_application}
	return render(request, 'leave/decline.html', context)


@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage'])
def process_leave_pass_view(request,id):
	instance = LeaveApplication.objects.get(id=id)
	var_status=6 # status=active
	if instance.status.status=='partly in process':
		var_status=2 # status=partly active
	LeaveApplication.objects.filter(id=id).update(
									status_id=var_status,approval_status_id=1)
	LeaveRecommendation.objects.create(leave_application_id=instance.id,
										created_by_id=request.user.id)
	return redirect('approved_leave')


@login_required(login_url='login')  
def resume_leave_view(request,id):
	current_status=LeaveApplication.objects.get(id=id).status
	resumption_approval_id=1
	groups=['head of unit','head of department','head of directorate']
	heads = User.objects.filter(id=request.user.id,user_group__group__in=groups)
	if heads:
		for user in heads:
			if user.user_group.group == 'head of unit':
				resumption_approval_id=2
			if user.user_group.group == 'head of department':
				resumption_approval_id=3
			elif user.user_group.group == 'head of directorate':
				resumption_approval_id=4
	status_id=3
	if current_status=='partly active':
		status_id=7
	LeaveApplication.objects.filter(id=id).update(
			resumption_approval_id=resumption_approval_id,status_id=status_id)# status='Resuming'
	return redirect('leave_history')


@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage','head of unit','head of department','head of directorate','support','developer'])
def list_resumption_view(request):
	leave_apps=None
	conditions=['resuming','partly resuming']
	dept_resumption_approval_id = ResumptionApproval.objects.get(approval='head of department').id
	if request.user.user_group.group=='leave_and_passage':
		leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id+2)
	groups=['head of unit','head of department','head of directorate']
	heads = User.objects.filter(id=request.user.id,user_group__group__in=groups)
	if heads:
		for user in heads:
			if user.user_group.group == 'head of unit':
				leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id-1,
							status__status__in=conditions,created_by__unit__id=request.user.unit.id)
			if user.user_group.group == 'head of department':
				leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id,
							status__status__in=conditions,created_by__department__id=request.user.department.id)
			elif user.user_group.group == 'head of directorate':
				leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id+1,
							status__status__in=conditions)
					
	context = {"leave_apps":leave_apps}
	return render(request, 'leave/list_pending_resumption.html', context)


@login_required(login_url='login')
@allowed_users(alllowed_roles=['head of unit','head of department','head of directorate'])
def recommend_resumption_view(request,id):
	current_resumption_approval=None
	# for app in leave_application:
	leave_application = LeaveApplication.objects.get(id=id)
	current_resumption_approval = leave_application.resumption_approval.id
	obj=LeaveResumption.objects.create(
					leave_application_id=id,recommended_by_id=request.user.id)
	obj.save()
	groups=['head of unit','head of department','head of directorate']
	heads = User.objects.filter(id=request.user.id,user_group__group__in=groups)
	if heads:
		for user in heads:
			if user.user_group.group == 'head of unit':
				LeaveApplication.objects.filter(id=id).update(
					resumption_approval_id=current_resumption_approval+1)
			elif user.user_group.group == 'head of department':
				LeaveApplication.objects.filter(id=id).update(
					resumption_approval_id=current_resumption_approval+1)
			else:
				LeaveApplication.objects.filter(id=id).update(
					resumption_approval_id=current_resumption_approval+1)
	
	return redirect('list_resumption')


@login_required(login_url='login')
def leave_history_view(request):
	app_status=['active','partly active','done','partly done','declined','resuming','partly resuming']
	leave_applications = LeaveApplication.objects.filter(created_by__id=request.user.id,
							status__status__in=app_status).order_by('-id')
	last_app = leave_applications.first() #bcos the leave apps are ordered in desc order
	current_desk='Leave & Passage'
	if last_app:
		if last_app.resumption_approval:
			if last_app.resumption_approval.approval=='head of unit':
				current_desk = f'Head of {request.user.unit.title}'
			if last_app.resumption_approval.approval=='head of department':
				current_desk = f'Head of {request.user.department.title}'
			elif last_app.resumption_approval.approval=='directorate':
				# current_desk = f'{request.user.department.directorate.title}'
				current_desk = 'Head of Admin'
	if request.method == 'POST':
		return redirect('index')
	context = {"leave_applications":leave_applications,"current_desk":current_desk}
	return render(request, 'leave/leave_history.html', context) 
	

@login_required(login_url='login')
def leave_details_view(request,id):
	cont,address=None,None
	detail = LeaveApplication.objects.get(id=id)
	user = User.objects.get(id=detail.created_by.id)
	emply = EmploymentDetails.objects.get(user=user)
	try:
		cont = Contact.objects.get(user=user)
	except ObjectDoesNotExist:
		pass
	try:
		address = Address.objects.get(user=user)
	except ObjectDoesNotExist:
		pass   
	context= {'user':user, 'emply':emply, 'cont':cont, 'address':address, 'detail':detail}
	return render(request, 'leave/leave_details.html', context)


@login_required(login_url='login')
def leave_status_detail(request):
	user=request.user.id
	_status=['in process','partly in process']
	recommendations = LeaveRecommendation.objects.filter(
									leave_application__status__status__in=_status,
									leave_application__created_by__id=user)
	
	context={"recommendations":recommendations}
	return render(request,'leave/leave_status_detail.html',context)


@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage'])
def acknowledge_leave_resumption_view(request,id):
	leave_application = LeaveApplication.objects.get(id=id)
	current_status=leave_application.status
	status_id=4
	if current_status=='resuming':
		status_id=8
	LeaveApplication.objects.filter(id=id).update(status_id=status_id,
		resumption_approval_id=5 # update to resumption_approval=resumed
	 )
	return redirect('list_resumption')	

@login_required(login_url='login')
def list_declined_applications_view(request):
	declined_apps = DeclineLeaveApplication.objects.filter(
		leave_application__created_by__id=request.user.id,
		leave_application__status__status='declined').order_by('-id')
	return render(request,'leave/declined_apps.html',{"declined_apps":declined_apps})

@login_required(login_url='login')
@allowed_users(alllowed_roles=['developer','support'])
def create_unit(request):
	departments = Department.objects.all()
	if request.method == 'POST':
		title = request.POST['title']
		department = request.POST['department']
		unit = Unit(title=title,department_id=department)
		unit.save()
		messages.success(request,"Unit add successfull")
	return render(request, 'leave/create_unit.html' ,{'departments':departments})

@login_required(login_url='login')
@allowed_users(alllowed_roles=['developer','support'])
def create_department(request):
	directorates = Directorate.objects.all()
	if request.method == 'POST':
		title = request.POST['title']
		directorate = request.POST['directorate']
		has_unit = request.POST.get('has_unit')
		if has_unit:
			department = Department(title=title,directorate_id=directorate)
			department.save()
		else:
			department = Department(title=title,directorate_id=directorate,has_unit=False)
			department.save()
		messages.success(request,"Department add successfull")
	return render(request, 'leave/create_department.html',{'directorates':directorates})


#======== render pdf view start ==============
@login_required(login_url='login')
def approved_leave_appcation_list(request):
	_status = ['active','partly active']	
	leave_applications = LeaveApplication.objects.filter(status__status__in=_status).order_by('-id')
	context ={'leave_applications':leave_applications} 	
	return render(request, 'leave/approved_leave_appcation.html',context)  


@login_required(login_url='login')
def user_approved_application_list(request):
	_status = ['active','partly active']	
	leave_applications = LeaveApplication.objects.filter(
						status__status__in=_status,created_by_id=request.user.id)
	context ={'leave_applications':leave_applications} 	
	return render(request, 'leave/approved_leave_appcation.html',context)


@login_required(login_url='login')
def render_pdf_view(request,id):
	emp_detail=None	
	leave_pass = LeaveApplication.objects.get(id=id)
	emp_detail = EmploymentDetails.objects.get(user_id=leave_pass.created_by.id)
	try:
		head_of_dept = User.objects.filter(user_group__group='head of department',
			department_id=leave_pass.created_by.department.id).last()
		head_of_admin=User.objects.get(file_number=2)
		processed_by=LeaveRecommendation.objects.filter(leave_application_id=leave_pass.id).last()
	except ObjectDoesNotExist:
		pass
	template_path = 'leave/pass.html'
	context = {'pass': leave_pass,"emp_detail":emp_detail,'processed_by':processed_by,
				"head_of_admin":head_of_admin, "head_of_dept":head_of_dept,
				"logo":f'{settings.HOST_SERVER}{settings.MEDIA_URL}/fmclogo.png'}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="leave.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)
	# create a pdf
	pisa_status = pisa.CreatePDF(html, dest=response)
	# if error then show some funy view
	if pisa_status.err:
	   return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response
#========= ends here =================

@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage','developer','support'])
def leave_tracker_view(request,id):
	status=['in process','partly in process']
	leave_app=None
	try:
		leave_app = LeaveApplication.objects.get(
					created_by_id=id,status__status__in=status)
	except ObjectDoesNotExist:
		pass
	approval_desk,approval_desk_id=None,None
	excluded = [1,2,6,7]
	if leave_app:
		approval_desk = leave_app.approval_status
		approval_desk_id = leave_app.approval_status.id
	approval_status = Approval.objects.all().exclude(id__in=excluded).order_by('-id')
	progress_bar_width=100/1
	if int(len(approval_status)) > 0:
		progress_bar_width=100/int(len(approval_status))
	declined_app = LeaveApplication.objects.filter(created_by_id=id).last()

	recommendations = LeaveRecommendation.objects.filter(
									leave_application__status__status__in=status,
									leave_application__created_by__id=id)

	context={"approval_desk":approval_desk,"approval_desk_id":approval_desk_id,
			"approval_status":approval_status,"declined_app":declined_app,"leave_app":leave_app,
			"progress_bar_width":progress_bar_width,"recommendations":recommendations}
	
	return render(request,'leave/leave_tracker.html',context)