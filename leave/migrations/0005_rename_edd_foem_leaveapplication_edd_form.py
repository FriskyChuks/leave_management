# Generated by Django 4.2.1 on 2023-07-17 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_leaveapplication_edd_foem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaveapplication',
            old_name='edd_foem',
            new_name='edd_form',
        ),
    ]