# Generated by Django 4.1.4 on 2023-01-03 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_class_options_rename_subject_student_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher_set', to='school.class')),
                ('class_arm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher_set', to='school.classarm')),
                ('taught_arms', models.ManyToManyField(to='school.classarm')),
                ('taught_classes', models.ManyToManyField(to='school.class')),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.teacher'),
        ),
    ]
