# Generated by Django 4.0.5 on 2022-08-22 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0002_gradelevel_created_by_salaryscale_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradelevel',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='salaryscale',
            name='created_by',
        ),
    ]
