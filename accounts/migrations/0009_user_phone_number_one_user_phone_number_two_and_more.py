# Generated by Django 4.0.3 on 2022-05-31 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_sub_unit_alter_user_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number_one',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number_two',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
