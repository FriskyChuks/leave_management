# from enum import unique
from django.db import models
from django.contrib.auth.models import User
from registry.models import *
from accounts.models import *
from contact.models import State
from django.utils import timezone

# Create your models here.


class LeaveType(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Approval(models.Model):
    approval = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.approval


class ResumptionApproval(models.Model):
    approval = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.approval


class LeaveDuration(models.Model):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    staff_category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE)
    duration = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.leave_type} leave | {self.duration} days"


class LeaveApplicationStatus(models.Model):
    status = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.status)


class LeaveApplication(models.Model):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.DO_NOTHING)
    leave_duration = models.ForeignKey(
        LeaveDuration, on_delete=models.DO_NOTHING)
    requested_duration = models.IntegerField()
    destination = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    date_from = models.DateField(null=True, auto_now_add=False, auto_now=False)
    date_to = models.DateField(null=True, auto_now_add=False, auto_now=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(
        LeaveApplicationStatus, on_delete=models.DO_NOTHING)
    auto = models.BooleanField(default=True)
    approval_status = models.ForeignKey(Approval, on_delete=models.DO_NOTHING)
    resumption_approval = models.ForeignKey(
        ResumptionApproval, null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    resumption_initiated = models.DateTimeField(null=True, blank=True)
    requires_hcs_approval = models.BooleanField(default=False)
    edd_form = models.ImageField(
        upload_to='eddform', null='True', blank='True')

    def __str__(self):
        return f"{self.leave_type} leave || {self.created_by.first_name} {self.created_by.last_name}"

    def current_year_leave(self):
        return timezone.now().year == self.date_from.year


class LeaveRecommendation(models.Model):
    leave_application = models.ForeignKey(
        'LeaveApplication', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.created_by.first_name} {self.created_by.last_name}")


class DeclineLeaveApplication(models.Model):
    leave_application = models.ForeignKey(
        'LeaveApplication', on_delete=models.CASCADE)
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.leave_application)


class LeaveResumption(models.Model):
    leave_application = models.ForeignKey(
        'LeaveApplication', on_delete=models.CASCADE)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.leave_application)
