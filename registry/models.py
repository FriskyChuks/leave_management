from django.db import models
from accounts.models import User


class StaffCategory(models.Model):
    title = models.CharField(max_length=6)
    def __str__(self):
        return self.title

class SalaryScale(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class GradeLevel(models.Model):
    level = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.level)


class EmploymentDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ministry = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    salary_scale = models.ForeignKey(SalaryScale, on_delete=models.CASCADE)
    staff_category = models.ForeignKey(StaffCategory, on_delete=models.CASCADE)
    grade = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    step = models.IntegerField()
    ippis_no = models.IntegerField(unique=True)
    def __str__(self):
        return str(self.user)
      