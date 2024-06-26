# Generated by Django 4.2.6 on 2023-10-30 16:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0003_remove_event_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='guests',
            new_name='attending_guests',
        ),
        migrations.AddField(
            model_name='event',
            name='invited_guests',
            field=models.ManyToManyField(blank=True, related_name='inviting_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
