# Generated by Django 4.0.5 on 2022-08-22 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.department'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='directorate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.directorate'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.gender'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='grade_level',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='accounts.gradelevel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='salary_scale',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.salaryscale'),
            preserve_default=False,
        ),
    ]