from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register (LeaveType)
admin.site.register (LeaveDuration)
# admin.site.register (LeaveProcess)
admin.site.register (LeaveApplicationStatus)
admin.site.register (LeaveResumption)
admin.site.register (LeaveRecommendation)
admin.site.register (LeaveApplication)
admin.site.register (Approval)
admin.site.register (DeclineLeaveApplication)
admin.site.register(ResumptionApproval)