# Generated by Django 4.1.4 on 2023-01-05 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_score_last_edited_alter_score_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
