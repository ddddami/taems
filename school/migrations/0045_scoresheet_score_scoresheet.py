# Generated by Django 4.1.7 on 2023-06-10 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0044_alter_score_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScoreSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.session')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.teacher')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.term')),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='scoresheet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.scoresheet'),
            preserve_default=False,
        ),
    ]
