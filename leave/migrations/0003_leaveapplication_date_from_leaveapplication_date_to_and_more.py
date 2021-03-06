# Generated by Django 4.0.3 on 2022-05-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_alter_leaveprocess_date_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='date_from',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='date_to',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='leaveresumption',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='leaveresumption',
            name='last_updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
