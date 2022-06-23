from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


# @receiver(post_save, sender=LeaveApplication)
# def post_save_create_or_update_recommendation(sender,instance,created,**kwargs):
#     if created:
#         print(instance.id)
