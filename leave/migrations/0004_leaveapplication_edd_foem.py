# Generated by Django 4.2.1 on 2023-07-17 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_leaveapplication_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='edd_foem',
            field=models.ImageField(blank='True', null='True', upload_to='eddform'),
            preserve_default='True',
        ),
    ]
