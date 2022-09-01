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
from django.views import View
from xhtml2pdf import pisa

from accounts.decorators import allowed_users
from .logics import *
from .models import *
from .forms import *
from registry.models import *
from contact.models import *


@login_required(login_url='login')
@allowed_users(alllowed_roles=['support'])
def leave_type(request):
	form = LeaveTypeForm()
	if request.method == 'POST':
		form = LeaveTypeForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('index')
	context = {'form':form} 
	return render(request, 'leave/leavetype.html', context)

@login_required(login_url='login')
@allowed_users(alllowed_roles=['support'])
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
	try:
		emp_details=EmploymentDetails.objects.get(user_id=request.user.id)
		if not emp_details.grade or not emp_details.ippis_no or not emp_details.designation:
			messages.info(request,"Please update your record before you continue")
			return redirect('edit_employment_detail',emp_details.id)
	except ObjectDoesNotExist:
		return redirect('employment_detail',request.user.id)   
	# check for active leave 
	if len(check_for_active_leave(request))>=1:
		messages.error(request, "You are not eligible for a leave now; you have an active leave")
		return redirect('index')    
	states = State.objects.all()
	leave_type = LeaveType.objects.get(id=id)
	
	user = request.user
	this_year = datetime.now()
	approval_status=Approval.objects.get(approval='none')
	no_of_days_used = LeaveApplication.objects.filter(
		created_by_id=user,leave_type_id=id,date_from__year=this_year.year).exclude(approval_status=approval_status)
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
@allowed_users(alllowed_roles=['leave_and_passage','head','developer'])	
def list_pending_leave_applications(request):
	leave_apps=None
	user = User.objects.get(id=request.user.id) 
	heads=Head.objects.filter(user_id=user)
	sub_unit_approval_status = Approval.objects.get(id=6)
	id=sub_unit_approval_status.id
	excluded_status=['done','partly done']
	# for leave & passage staff
	if request.user.user_group.group=='leave_and_passage':
		leave_apps = LeaveApplication.objects.filter(approval_status_id=id-4).exclude(status_id=8)
	
	# if head.is_head_of_sub_unit:
	# 	leave_apps = LeaveApplication.objects.filter(approval_status_id=id,
	# 				created_by__sub_unit__id=request.user.sub_unit.id).exclude(status_id=8)
	for head in heads:
		if head.is_head_of_unit: 
			leave_apps = LeaveApplication.objects.filter(approval_status_id=id-1,
								created_by__unit__id=request.user.unit.id).exclude(status__status=excluded_status) 
		elif head.is_head_of_dept:
			leave_apps = LeaveApplication.objects.filter(approval_status_id=id-2,
					created_by__department__id=request.user.department.id).exclude(status__status=excluded_status)
		elif head.is_head_of_directorate:    
				leave_apps = LeaveApplication.objects.filter(approval_status_id=id-3,
					created_by__directorate__id=request.user.directorate.id).exclude(status__status=excluded_status)

	context = {'leave_apps': leave_apps}
	return render(request, 'leave/list_pending_leave_applications.html', context)    


@login_required(login_url='login')
@allowed_users(alllowed_roles=['head','support','developer'])
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
@allowed_users(alllowed_roles=['head','support','developer'])
def decline_leave_application(request,id):
	leave_application = LeaveApplication.objects.get(id=id)
	_status = LeaveApplicationStatus.objects.get(status='declined')
	approval_status=Approval.objects.get(approval='none')
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
@allowed_users(alllowed_roles=['leave_and_passage','developer'])
def process_leave_pass_view(request,id):
	# Update status=active or partly_active, approval=none and resumption_approval=default
	instance = LeaveApplication.objects.get(id=id)
	var_status=6 # status=active
	if instance.status.status=='partly in process':
		var_status=2 # status=partly active
	LeaveApplication.objects.filter(id=id).update(
		status_id=var_status,approval_status_id=1,resumption_approval=4 
	 )
	return redirect('approved_leave')


@login_required(login_url='login')  
def resume_leave_view(request,id):
	current_status=LeaveApplication.objects.get(id=id).status
	head=get_heads_of_locations(request)
	resumption_approval_id=1
	if head:
		if head.is_head_of_dept:
			resumption_approval_id=2
		elif head.is_head_of_directorate:
			resumption_approval_id=3
	status_id=3
	if current_status=='partly active':
		status_id=7
	LeaveApplication.objects.filter(id=id).update(resumption_approval_id=resumption_approval_id,
									status_id=status_id)# status='Resuming'
	return redirect('leave_history')


@login_required(login_url='login')
@allowed_users(alllowed_roles=['leave_and_passage','head','support','developer'])
def list_resumption_view(request):
	leave_apps=None
	conditions=['resuming','partly resuming']
	heads = Head.objects.filter(user_id=request.user.id)
	dept_resumption_approval_id = ResumptionApproval.objects.get(approval='head of department').id
	if request.user.user_group.group=='leave_and_passage':
		leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id+2)
	for head in heads:
		if head.is_head_of_dept:
			leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id,
						status__status__in=conditions,created_by__department__id=request.user.department.id)
		elif head.is_head_of_directorate:
			leave_apps = LeaveApplication.objects.filter(resumption_approval_id=dept_resumption_approval_id+1,
						status__status__in=conditions,created_by__directorate__id=request.user.directorate.id)
				
	context = {"leave_apps":leave_apps}
	return render(request, 'leave/list_pending_resumption.html', context)


@login_required(login_url='login')
def recommend_resumption_view(request,id):
	current_resumption_approval=None
	# for app in leave_application:
	leave_application = LeaveApplication.objects.get(id=id)
	current_resumption_approval = leave_application.resumption_approval.id
	obj=LeaveResumption.objects.create(
					leave_application_id=id,recommended_by_id=request.user.id)
	obj.save()
	head=get_heads_of_locations(request)
	if head.is_head_of_directorate:
		LeaveApplication.objects.filter(id=id).update(
			resumption_approval_id=current_resumption_approval+1)
	else:
		LeaveApplication.objects.filter(id=id).update(
			resumption_approval_id=current_resumption_approval+1)
	
	return redirect('list_resumption')


@login_required(login_url='login')
def leave_history_view(request):
	included=['active','partly active','done','partly done','declined','resuming','partly resuming']
	leave_applications = LeaveApplication.objects.filter(created_by__id=request.user.id,
							status__status__in=included).order_by('-id')
	last_app = leave_applications.last()
	current_desk='Leave & Passage'
	if last_app:
		if last_app.resumption_approval:
			if last_app.resumption_approval.approval=='head of department':
				current_desk='Head of Dept'
			elif last_app.resumption_approval.approval=='directorate':
				current_desk='Head of Admin'
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
		resumption_approval_id=4 # update to resumption_approval=resumed
	 )
	return redirect('list_resumption')	


def list_declined_applications_view(request):
	declined_apps = DeclineLeaveApplication.objects.filter(
		leave_application__created_by__id=request.user.id,
		leave_application__status__status='declined').order_by('-id')
	return render(request,'leave/declined_apps.html',{"declined_apps":declined_apps})


#======== render pdf view start ==============

def approved_leave_appcation_list(request):
	leave_status = LeaveApplicationStatus.objects.get(id=2)	
	leave_applications = LeaveApplication.objects.filter(status =leave_status)	
	context ={'leave_applications':leave_applications} 	
	return render(request, 'leave/approved_leave_appcation.html',context)  

def render_pdf_view(request,id):
	emp_detail=None	
	leave_pass = 	LeaveApplication.objects.get(id=id)
	emp_detail = EmploymentDetails.objects.get(user_id=leave_pass.created_by.id)
	try:
		head_of_dept = Head.objects.get(is_head_of_dept=True,
			user_id__department__id=leave_pass.created_by.department.id)
		head_of_admin = Head.objects.get(is_head_of_directorate=True,
			user_id__directorate__id=leave_pass.created_by.department.directorate.id)
	except ObjectDoesNotExist:
		pass
	template_path = 'leave/pass.html'
	context = {'pass': leave_pass,"emp_detail":emp_detail,"head_of_dept":head_of_dept,
				"head_of_admin":head_of_admin}
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