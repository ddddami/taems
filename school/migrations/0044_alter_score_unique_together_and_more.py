# Generated by Django 4.1.7 on 2023-06-10 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0043_student_school_teacher_school_alter_school_logo_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='score',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='score',
            name='session',
        ),
        migrations.RemoveField(
            model_name='score',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='score',
            name='term',
        ),
    ]
