# Generated by Django 4.0.5 on 2022-10-17 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_delete_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='other_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]