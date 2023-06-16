from django.shortcuts import render
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from leave.models import *
from registry.models import SalaryScale,GradeLevel


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
	_resumption_status = ['head of unit','head of department','directorate','none']
	now = timezone.now()
	due_resumptions = LeaveApplication.objects.aggregate(
		# total=models.Count('id'),
		today=models.Count('id', filter=models.Q(date_to=now.date())),
		overdue=models.Count('id', filter=models.Q(date_to__lt=now.date(),
						resumption_approval__approval__in=_resumption_status))
	)
	return due_resumptions


def active_leave_list_view(request):
	status=['partly active','active']
	active_apps = None
	if request.user.user_group.group == 'head of unit':
		active_apps = LeaveApplication.objects.filter(status__status__in=status,
									created_by__unit_id=request.user.unit.id)
	elif request.user.user_group.group == 'head of department':
		active_apps = LeaveApplication.objects.filter(status__status__in=status,
									created_by__department_id=request.user.department.id)
	elif request.user.user_group.group == 'head of directorate':
		active_apps = LeaveApplication.objects.filter(status__status__in=status,
									created_by__directorate_id=request.user.directorate.id)

	context={'active_apps':active_apps}
	return render(request, 'reports/active_leave_list.html',context)


def general_leave_report(request):
	directorates=Directorate.objects.all()
	departments=Department.objects.all().order_by('title')
	units=Unit.objects.all().order_by('title')
	# salary_scales=SalaryScale.objects.all()
	# grades=GradeLevel.objects.all()
	leave_types = LeaveType.objects.all().order_by('title')
	leave_status = LeaveApplicationStatus.objects.all().order_by('status')

	file_no = request.GET.get('file_no')
	leave_type = request.GET.get('leave_type')
	status = request.GET.get('leave_status')
	# salary_scale = request.GET.get('salary_scale')
	date_from = request.GET.get('date_from')
	date_to = request.GET.get('date_to')
	directorate = request.GET.get('directorate')
	department = request.GET.get('department')
	unit = request.GET.get('unit')
	custom_search_from = request.GET.get('custom_search_from')
	custom_search_to = request.GET.get('custom_search_to')
	
	filters = {'created_by__file_number':file_no,'date_from': date_from,'date_to':date_to,
				'created_by__department__id':department,'created_by__directorate__id':directorate,
				'leave_type__id':leave_type,'status__status__icontains':status,'created_by__unit__id':unit,
				'date_from__gte':custom_search_from, 'date_to__lte':custom_search_to			
				}
	# date_filter = {'date_created__date':timezone.now()}
	filters = {k:v for k,v in filters.items() if v}
	if filters:
		leave_apps = LeaveApplication.objects.filter(**filters)
	else:
		leave_apps = LeaveApplication.objects.filter(date_created__date=timezone.now())
		
	context={"directorates":directorates,"departments":departments,"units":units,
			"leave_apps":leave_apps,"leave_types":leave_types,'leave_status':leave_status,
		}
	return render(request,'reports/general_leave_report.html',context)
