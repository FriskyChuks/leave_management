from django.shortcuts import render
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from leave.models import *


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