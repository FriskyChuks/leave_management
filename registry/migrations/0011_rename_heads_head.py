# Generated by Django 4.0.3 on 2022-05-24 12:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registry', '0010_heads'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Heads',
            new_name='Head',
        ),
    ]
