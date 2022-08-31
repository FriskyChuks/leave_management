from datetime import datetime
from dateutil.relativedelta import relativedelta

from leave.models import *

def get_heads_of_locations(request):
	head=Head.objects.get(user_id=request.user.id)
	return head

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
	approval_status=5
	heads = Head.objects.filter(user_id=request.user.id)
	if heads.exists():
		for head in heads:
			if head.is_head_of_directorate:
				approval_status=2
			elif head.is_head_of_dept:
				approval_status=3
			elif head.is_head_of_unit:
				approval_status=4
	return approval_status