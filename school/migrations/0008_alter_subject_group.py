# Generated by Django 4.1.4 on 2023-01-03 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_subjectgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.subjectgroup'),
        ),
    ]
