from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Event object
class Event(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=26)
    location = models.CharField(max_length=26)
    date = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    invited_guests = models.ManyToManyField(
        User, related_name='inviting_events', blank=True)
    attending_guests = models.ManyToManyField(
        User, related_name='attending_events', blank=True)

# Event invitation object


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        User, related_name='received_invitations', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

# Chat message object


class Message(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Friend request object


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_request', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        User, related_name='received_request', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

# Friend list object


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    requested_friends = models.ManyToManyField(
        User, related_name='requested_friends', blank=True)
    friends = models.ManyToManyField(
        User, related_name='friends', blank=True)
