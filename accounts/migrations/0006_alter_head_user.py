# Generated by Django 4.0.5 on 2022-08-30 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_department_has_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='head',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
