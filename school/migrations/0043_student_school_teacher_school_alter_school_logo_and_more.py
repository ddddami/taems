# Generated by Django 4.1.7 on 2023-06-08 22:03

from django.db import migrations, models
import django.db.models.deletion
import school.validators


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0042_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.school'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.school'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school',
            name='logo',
            field=models.ImageField(blank=True, default='school/images/school.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(default='school/images/user.png', null=True, upload_to='school/images', validators=[school.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='school/images/user.png', null=True, upload_to='school/images', validators=[school.validators.validate_file_size]),
        ),
    ]
