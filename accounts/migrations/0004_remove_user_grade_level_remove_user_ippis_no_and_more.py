# Generated by Django 4.0.5 on 2022-08-23 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_ippis_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='grade_level',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ippis_no',
        ),
        migrations.RemoveField(
            model_name='user',
            name='salary_scale',
        ),
    ]
