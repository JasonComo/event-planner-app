# Generated by Django 4.2.6 on 2023-10-27 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_event_guests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
    ]
