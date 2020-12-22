# Generated by Django 3.0.5 on 2020-12-21 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parents', '0006_tutorrequest_desired_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorrequest',
            name='desired_time',
        ),
        migrations.RemoveField(
            model_name='tutorrequest',
            name='inProgress',
        ),
        migrations.RemoveField(
            model_name='tutorrequest',
            name='isAccepted',
        ),
        migrations.RemoveField(
            model_name='tutorrequest',
            name='isRejected',
        ),
        migrations.RemoveField(
            model_name='tutorrequest',
            name='purpose_of_rejection',
        ),
        migrations.RemoveField(
            model_name='tutorrequest',
            name='subjects_requested',
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='isRated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='preferred_days',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
