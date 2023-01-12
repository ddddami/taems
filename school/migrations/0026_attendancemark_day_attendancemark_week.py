# Generated by Django 4.1.4 on 2023-01-05 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_attendancemark'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancemark',
            name='day',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.day'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendancemark',
            name='week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.week'),
            preserve_default=False,
        ),
    ]