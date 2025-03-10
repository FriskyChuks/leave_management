# from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=EmploymentDetails)
def post_save_update_staff_category(sender, instance, created, **kwargs):
    if instance.grade.level < 6 and instance.salary_scale.title == 'CONHESS':
        EmploymentDetails.objects.filter(id=instance.id).update(staff_category_id=1)# id of 1=Junior staff
    else:
        EmploymentDetails.objects.filter(id=instance.id).update(staff_category_id=2)# id of 2=Senior staff