from datetime import datetime
from dateutil.relativedelta import relativedelta

from leave.models import *

def check_leave_eligibility(request,leave_type_id):
	month_difference=12
	previous_leaves=LeaveApplication.objects.filter(
		created_by_id=request.user.id,leave_type_id=leave_type_id,status__status='done')
	if previous_leaves:
		last_leave_date=previous_leaves.last().date_to
		delta = relativedelta(datetime.today(), last_leave_date)
		month_difference =  delta.months + (delta.years * 12)
	return month_difference

def check_current_year(request,leave_type_id):
	same_year=False
	last_leave=LeaveApplication.objects.filter(created_by_id=request.user.id,
		leave_type_id=leave_type_id,status__status='done').last()
	if last_leave:
		if last_leave.date_from.year==datetime.now().date().year:
			same_year=True	
	return same_year
		  

def check_for_active_leave(request):
	excluded = ['done','declined','partly done']
	active_leave = LeaveApplication.objects.filter(created_by=request.user.id).exclude(
					status__status__in=excluded)
	return active_leave

def check_if_user_is_head(request):
	approval_status= Approval.objects.get(approval='head of unit').id # id=4
	groups=['head of unit','head of department','head of directorate']
	heads = User.objects.filter(id=request.user.id,user_group__group__in=groups)
	if heads:
		for user in heads:
			if user.user_group.group == 'head of directorate':
				approval_status=Approval.objects.get(approval='head of directorate').id # id=2
			elif user.user_group.group == 'head of department':
				approval_status=Approval.objects.get(approval='head of department').id # id=3
			# elif user.user_group.group == 'head of unit':
			# 	approval_status=Approval.objects.get(approval='head of unit').id # id=4
	return approval_status


def has_annual_leave(id):
	today = datetime.now()
	status=['done','partly done']
	total_duration=0
	annual_leaves=LeaveApplication.objects.filter(date_from__year=today.year,
							leave_type__title__icontains='annual',
							created_by_id=id,status__status__in=status)
	for annual_leave in annual_leaves:
		duration=annual_leave.requested_duration
		total_duration += duration	
	return total_duration