# Generated by Django 4.1.5 on 2023-01-27 20:11

from django.db import migrations, models
import school.validators


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0037_student_image_teacher_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(null=True, upload_to='school/images', validators=[school.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(null=True, upload_to='school/images', validators=[school.validators.validate_file_size]),
        ),
    ]
