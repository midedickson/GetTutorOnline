# Generated by Django 3.0.5 on 2020-10-30 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0009_auto_20201027_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutoringplan',
            name='desired_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
