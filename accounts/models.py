from django.db import models
from django.contrib.auth.models import AbstractUser

# from registry.models import GradeLevel, SalaryScale


class UserGroup(models.Model):
    group = models.CharField(max_length=50)

    def __str__(self):
        return self.group


class Gender(models.Model):
    title = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self):
        return self.title


class GradeLevel(models.Model):
    level = models.IntegerField()

    def __str__(self):
        return str(self.level)


class SalaryScale(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Directorate(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Department(models.Model):
    title = models.CharField(max_length=50, unique=True)
    directorate = models.ForeignKey(Directorate, on_delete=models.CASCADE)
    has_unit = models.BooleanField(default=True)
    reports_to_cmd = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SubUnit(models.Model):
    title = models.CharField(max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    other_name = models.CharField(blank=True, null=True, max_length=50)
    file_number = models.IntegerField(unique=True, blank=True, null=True)
    username = models.CharField(unique=True, max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    directorate = models.ForeignKey(Directorate, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, null=True, blank=True)
    user_group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, blank=True, null=True)
    passport = models.ImageField(
        upload_to='passport', null=True, blank=True, default="default.jpg")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'other_name', 'file_number',
                       'date_of_birth', 'gender', 'directorate', 'department')

    def __str__(self):
        return str(self.username)

    @property
    def imageURL(self):
        try:
            url = self.passport.url
        except:
            url = ''
        return url
