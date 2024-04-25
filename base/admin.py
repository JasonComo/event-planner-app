from django.contrib import admin

# Register your models here.

from .models import Event, Invitation, Message, FriendRequest, FriendList

admin.site.register(Event)
admin.site.register(Invitation)
admin.site.register(Message)
admin.site.register(FriendRequest)
admin.site.register(FriendList)
