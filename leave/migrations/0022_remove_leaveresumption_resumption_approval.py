# Generated by Django 4.0.5 on 2022-06-28 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0021_leaveapplication_resumption_approval'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaveresumption',
            name='resumption_approval',
        ),
    ]