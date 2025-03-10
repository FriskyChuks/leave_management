from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
# import datetime

from leave.models import *

# def get_working_days(d1,d2,n):
# 	if int(n) == int(np.busday_count( d1, d2 )):
# 		print(n)
# 	else:
# 		print("Not equal")
# 	return int(n)


def date_by_adding_business_days(from_date, add_days, holidays):
    business_days_to_add = add_days
    current_date = datetime.strptime(from_date, "%Y-%m-%d")
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        if current_date in holidays:
            continue
        business_days_to_add -= 1
    print(current_date)
    return current_date


def check_leave_eligibility(request, leave_type_id):
    month_difference = 12
    previous_leaves = LeaveApplication.objects.filter(
        created_by_id=request.user.id, leave_type_id=leave_type_id, status__status='done')
    if previous_leaves:
        last_leave_date = previous_leaves.last().date_from
        delta = relativedelta(datetime.today(), last_leave_date)
        month_difference = delta.months + (delta.years * 12)
    return month_difference


def check_current_year(request, leave_type_id):
    same_year = False
    last_leave = LeaveApplication.objects.filter(created_by_id=request.user.id,
                                                 leave_type_id=leave_type_id, status__status='done').last()
    if last_leave:
        if last_leave.date_from.year == datetime.now().date().year:
            same_year = True
    return same_year


def check_for_active_leave(request):
    excluded = ['done', 'declined', 'partly done']
    active_leave = LeaveApplication.objects.filter(created_by=request.user.id).exclude(
        status__status__in=excluded)
    return active_leave


def check_if_user_is_head(request):
    approval_status = Approval.objects.get(approval='head of unit').id  # id=4
    groups = ['head of unit', 'head of department',
              'head of directorate', 'cmd']
    heads = User.objects.filter(
        id=request.user.id, user_group__group__in=groups)
    if heads:
        for user in heads:
            if user.user_group.group == 'head of directorate' or user.user_group.group == 'cmd':
                approval_status = int(approval_status)-3
            elif user.user_group.group == 'head of department':
                approval_status = int(approval_status)-2
            elif user.user_group.group == 'head of unit':
                approval_status = int(approval_status)-1
    else:
        if not request.user.department.has_unit:
            approval_status = int(approval_status)-1
    return approval_status


def has_annual_leave(id):
    today = datetime.now()
    status = ['done', 'partly done']
    total_duration = 0
    annual_leaves = LeaveApplication.objects.filter(date_from__year=today.year,
                                                    leave_type__title__icontains='annual',
                                                    created_by_id=id, status__status__in=status)
    for annual_leave in annual_leaves:
        duration = annual_leave.requested_duration
        total_duration += duration
    return int(total_duration)


def holidays():
    dt = datetime
    Holidays = [dt(2024, 12, 25),dt(2024, 12, 26),dt(2025, 1, 1),dt(2025, 3, 31),dt(2025, 4, 1),dt(2025, 4, 21),dt(2025, 5, 1),
                dt(2025, 6, 7),dt(2025, 6, 8),dt(2025, 6, 12),dt(2025, 9, 5),dt(2025, 10, 1),dt(2025, 12, 25),dt(2025, 12, 26),
                dt(2026, 1, 1)]

    return Holidays
