# Generated by Django 4.1.4 on 2023-01-12 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0034_student_middle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='last_name',
        ),
    ]
