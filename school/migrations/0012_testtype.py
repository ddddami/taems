# Generated by Django 4.1.4 on 2023-01-04 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('CA', 'Continuous Assessment'), ('EX', 'Examination')], max_length=255)),
            ],
        ),
    ]