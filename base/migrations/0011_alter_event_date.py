# Generated by Django 4.2.6 on 2023-11-13 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default='11/13/2023'),
        ),
    ]
