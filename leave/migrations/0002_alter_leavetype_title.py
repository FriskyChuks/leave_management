# Generated by Django 4.0.5 on 2022-10-11 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetype',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]