# Generated by Django 4.0.3 on 2022-06-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_address_state_of_residence_contact_nationality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='next_of_kin',
            field=models.CharField(max_length=50),
        ),
    ]
