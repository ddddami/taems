# Generated by Django 4.1.4 on 2023-01-05 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_term_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
