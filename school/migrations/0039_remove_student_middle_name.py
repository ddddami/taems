# Generated by Django 4.1.5 on 2023-01-30 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0038_alter_student_image_alter_teacher_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='middle_name',
        ),
    ]