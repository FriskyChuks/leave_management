from django.db import models
from accounts.models import User


class StaffCategory(models.Model):
    title = models.CharField(max_length=6)

    def __str__(self):
        return self.title


class SalaryScale(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class GradeLevel(models.Model):
    level = models.IntegerField()

    def __str__(self):
        return str(self.level)


class EmploymentDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ministry = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, null=True, blank=True)
    salary_scale = models.ForeignKey(SalaryScale, on_delete=models.CASCADE)
    staff_category = models.ForeignKey(
        StaffCategory, on_delete=models.CASCADE, null=True, blank=True)
    grade = models.ForeignKey(
        GradeLevel, on_delete=models.CASCADE, null=True, blank=True)
    step = models.IntegerField(null=True, blank=True)
    ippis_no = models.IntegerField(null=True, blank=True)
    qualifications = models.CharField(max_length=225, blank=True, null=True)
    rank = models.CharField(max_length=225, blank=True, null=True)
    first_appointment_date = models.DateField(blank=True, null=True)
    confirmation_date = models.DateField(blank=True, null=True)
    date_of_appt_with_fmc = models.DateField(blank=True, null=True)
    present_appt_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.user)
