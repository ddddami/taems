# Generated by Django 4.1.4 on 2023-01-05 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0028_alter_attendancemark_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='title',
            field=models.CharField(default='First Week', max_length=255),
            preserve_default=False,
        ),
    ]
