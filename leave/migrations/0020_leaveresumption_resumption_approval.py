# Generated by Django 4.0.5 on 2022-06-28 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0019_resumptionapproval'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveresumption',
            name='resumption_approval',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='leave.resumptionapproval'),
            preserve_default=False,
        ),
    ]