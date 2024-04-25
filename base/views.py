from django.shortcuts import render
from .models import FriendList
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Invitation, Event, User, Message, FriendRequest, FriendList
from .forms import EventForm, UserRegistrationForm, AddFriendForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Function to register a user


def register(request):
    # Check if request method is POST
    if request.method == 'POST':
        # If it is, create form instance
        form = UserRegistrationForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Create new user by saving form data
            new_user = form.save()

            # Clear friend list
            friend_list = FriendList.objects.create(user=new_user)
            friend_list.requested_friends.clear()
            friend_list.friends.clear()

            # Redirect home
            return redirect('home')

    else:
        # If the request method is not POST, create an empty form instance
        form = UserRegistrationForm()

    # Render registration page with the form
    return render(request, 'registration/register.html', {'form': form})


# Function to load the home page
@login_required
def home(request):

    # Define user
    user = request.user

    # Get user's friend requests
    friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get user's invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get user's events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Create context of all relevant user info
    context = {
        'friend_requests': friends_requests,
        'invitations': invitations,
        'events': events,
        'show_create_event_form': False,
        'show_edit_event_form': False,
        'show_friends': False,
        'show_view_event': False,
    }

    # Render the home page with the user's context
    return render(request, 'base/index.html', context)


# Function to view an event
@login_required
def view_event(request, event_id):

    # Define user
    user = request.user

    # Get user's friend requests
    friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get user's invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get user's events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Define the event being viewed
    event = get_object_or_404(Event, pk=event_id)

    # Get the chat messages for the event
    messages = event.message_set.all()

    # Create context of all relevant user and event info
    context = {'event': event, 'messages': messages, 'friend_requests': friends_requests,
               'invitations': invitations,
               'events': events,         'show_create_event_form': True,
               'show_view_event': True,
               'show_edit_event_form': False,
               'show_friends': False}

    # Render the view-event page wit the appropriate context
    return render(request, 'base/view-event.html', context)

# Function to create an event.


@login_required
def create_event(request):

    # Define user
    user = request.user

    # Get user's friend requests
    friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get user's invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get user's events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Check if request method is POST
    if request.method == 'POST':
        # If it is, create form instance
        form = EventForm(request.POST, user=request.user)

        # Check if form is valid
        if form.is_valid():

            # If it is, create event
            event = form.save(commit=False)

            # Define event organizer as the user
            event.organizer = request.user

            # Save the event
            event.save()
            form.save_m2m()

            # Get the guest list
            guest_list = event.invited_guests.all()

            # Send invitations to the guests
            for guest in guest_list:
                invitation = Invitation(
                    event=event, sender=event.organizer, recipient=guest)
                invitation.save()

            # Redirect to home page
            return redirect('home')
    else:
        # If the request method is not POST, create an empty form instance
        form = EventForm(user=request.user)

    # Create context of all relevant user and event info
    context = {
        'friend_requests': friends_requests,
        'invitations': invitations,
        'events': events,
        'show_create_event_form': True,
        'show_view_event': False,
        'show_edit_event_form': False,
        'show_friends': False,
        'form': form
    }

    # Render the create-event page wit the appropriate context
    return render(request, 'base/create-event.html', context)

# Function to edit an event


@login_required
def edit_event(request, event_id):
    # Define the user
    user = request.user

    # Get user's friend requests
    friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get user's invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get user's events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Get the event to edit
    event = get_object_or_404(Event, id=event_id)

    # Check if request method is POST
    if request.method == 'POST':
        # If it is, create form instance
        form = EventForm(request.POST, instance=event,
                         user=request.user, edit_mode=True)

        # Check if form is valid
        if form.is_valid():
            # If it is, save the event
            event = form.save()

            # Clear all previous invitations related to the event
            event.invitation_set.all().delete()

            # Update guest list
            guest_list = event.invited_guests.all()

            # Send new invitations to the updated guests
            for guest in guest_list:
                invitation = Invitation(
                    event=event, sender=event.organizer, recipient=guest)
                invitation.save()

            # Redirect to home page
            return redirect('home')
    else:
        # If the request method is not POST, create an empty form instance
        form = EventForm(instance=event, user=request.user,
                         edit_mode=True)

     # Create context of all relevant user and event info
    context = {
        'friend_requests': friends_requests,
        'invitations': invitations,
        'events': events,
        'show_create_event_form': False,
        'show_edit_event_form': True,
        'show_friends': False,
        'show_view_event': False,
        'form': form
    }

    # Render the create-event page wit the appropriate context
    return render(request, 'base/edit-event.html', context)

# Function to delete an event


@login_required
def delete_event(request, event_id):
    # Get the event to delete
    event = get_object_or_404(Event, id=event_id)
    # Check if request is POST
    if request.method == 'POST':
        # If it is, delete the event
        event.delete()

    # Redirect to home page
    return redirect('home')


# Function to leave an event
@login_required
def leave_event(request, event_id):
    # Define the user
    user = request.user

    # Get the event to delete
    event = get_object_or_404(Event, id=event_id)
    # Check if request is POST
    if request.method == 'POST':
        # If it is, remove the user from the event
        event.attending_guests.remove(user)

    # Redirect to home page
    return redirect('home')


# Function to accept an invitation to an event
@login_required
def accept_invitation(request, invitation_id):
    # Get the invitation
    invitation = Invitation.objects.get(id=invitation_id)

    # Check if request is POST
    if request.method == 'POST':

        # Define user's action
        action = request.POST.get('action')

        if action == 'accept':
            # If accepted, add user to attending guests and
            # remove them from invited guests
            event = invitation.event
            event.attending_guests.add(request.user)
            event.invited_guests.remove(request.user)
            invitation.accepted = True
            invitation.save()
        elif action == 'decline':
            # If declined, remove user from invited guests
            invitation.event.invited_guests.remove(request.user)
            invitation.delete()

    # Redirect to home page
    return redirect('home')

# Function to send a chat message


@login_required
def send_message(request, event_id):
    # Define the event that the chat message will be sent in
    event = get_object_or_404(Event, id=event_id)

    # Check if request is POST
    if request.method == 'POST':
        # If it is, get the message content
        message_content = request.POST.get('message')

        if message_content:
            # Create a message object
            new_message = Message(
                event=event, sender=request.user, content=message_content)
            new_message.save()

            # Optional success message
            messages.success(request, 'Message sent successfully.')

            # Redirect to view-event page with the event being viewed
            return redirect('view_event', event_id=event.id)

        else:
            # Optional error message
            messages.error(request, 'Message content cannot be empty.')

    # Render view-event page.
    return render(request, 'view_event.html', {'event': event})


# Function to view friends
@login_required
def view_friends(request):
    # Define user
    user = request.user

    # Get incoming friend requests
    received_friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get outgoing friend requests
    sent_friend_requests = FriendRequest.objects.filter(sender=user)
    friend_list = FriendList.objects.get(user=user)
    received_requests = received_friends_requests.all()
    sent_requests = sent_friend_requests.all()

    # Get friends
    friends = friend_list.friends.all()

    # Get invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Create context of all relevant user and event info
    context = {'invitations': invitations,
               'events': events, 'friends': friends, 'received_requests': received_requests, 'sent_requests': sent_requests,
               'show_create_event_form': False,
               'show_edit_event_form': False,
               'show_view_event': False,
               'show_friends': True}

    # Render friends page
    return render(request, 'base/friends.html', context)


# Function to add a friend
@login_required
def add_friend(request):
    # Define user
    user = request.user

    # Get invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Get incoming friend requests
    received_friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get outgoing friend requests
    sent_friend_requests = FriendRequest.objects.filter(sender=user)

    # Get friend list
    friend_list = FriendList.objects.get(user=user)

    # Define received and sent requests, and friends
    received_requests = received_friends_requests.all()
    sent_requests = sent_friend_requests.all()
    friends = friend_list.friends.all()

    # Create context of all relevant user and event info
    context = {'invitations': invitations,
               'events': events, 'friends': friends, 'received_requests': received_requests, 'sent_requests': sent_requests,
               'show_create_event_form': False,
               'show_edit_event_form': False,
               'show_view_event': False,
               'show_friends': True}

    # Check if request is POST
    if request.method == 'POST':
        # If it is, create form instance
        form = AddFriendForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Define and clean username
            username = form.cleaned_data['username']

            # Handle errors
            if username == user.username:
                form.add_error(
                    'username', 'You cannot add yourself as a friend.')
                context['form'] = form
            else:
                try:
                    recipient = User.objects.get(username=username)
                except User.DoesNotExist:
                    form.add_error(
                        'username', 'User with this username does not exist.')
                    context['form'] = form
                    return render(request, 'base/friends.html', context)

                # Check if the recipient is already in the friend list
                if recipient in friend_list.friends.all():
                    form.add_error(
                        'username', f'{recipient.username} is already your friend.')
                    context['form'] = form
                elif FriendRequest.objects.filter(sender=user, recipient=recipient, accepted=False).exists():
                    form.add_error(
                        'username', f'A friend request to {recipient.username} is already pending.')
                    context['form'] = form
                else:
                    # Proceed with sending the friend request
                    friend_request = FriendRequest(
                        sender=user, recipient=recipient)
                    friend_request.save()
                    friend_list.requested_friends.add(recipient)
                    friend_list.save()

            return render(request, 'base/friends.html', context)

    # If the request method is not POST, create an empty form instance
    form = AddFriendForm()
    context['form'] = form

    # Render friends page
    return render(request, 'base/friends.html', context)

# Function to remove a friend


@login_required
def remove_friend(request, friend_id):
    # Define user
    user = request.user

    # Get invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Get incoming friend requests
    received_friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get outgoing friend requests
    sent_friend_requests = FriendRequest.objects.filter(sender=user)

    # Get friend list
    friend_list = FriendList.objects.get(user=user)

    # Define received and sent requests, and friends
    received_requests = received_friends_requests.all()
    sent_requests = sent_friend_requests.all()
    friends = friend_list.friends.all()

    # Get friend to remove
    friend = get_object_or_404(User, id=friend_id)

    # Get friend's friend list
    receipient_friend_list = FriendList.objects.get(user=friend)

    # Create context of all relevant user and friend info
    context = {'invitations': invitations,
               'events': events, 'friends': friends, 'received_requests': received_requests, 'sent_requests': sent_requests,
               'show_create_event_form': False,
               'show_edit_event_form': False,
               'show_view_event': False,
               'show_friends': True}

    # Check if request is POST
    if request.method == 'POST':

        # If it is, remove friend and user from each other's friend list
        friend_list.friends.remove(friend)
        receipient_friend_list.friends.remove(user)

    # Render friend page
    return render(request, 'base/friends.html', context)

# Function to cancel a friend request


@login_required
def cancel_friend_request(request, friend_request_id):

    # Define user
    user = request.user

    # Get invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Get incoming friend requests
    received_friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get outgoing friend requests
    sent_friend_requests = FriendRequest.objects.filter(sender=user)

    # Get friend list
    friend_list = FriendList.objects.get(user=user)

    # Define received and sent requests, and friends
    received_requests = received_friends_requests.all()
    sent_requests = sent_friend_requests.all()
    friends = friend_list.friends.all()

    # Get friend request to cancel
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)

    # Create context of all relevant user and friend info
    context = {'invitations': invitations,
               'events': events, 'friends': friends, 'received_requests': received_requests, 'sent_requests': sent_requests,
               'show_create_event_form': False,
               'show_edit_event_form': False,
               'show_view_event': False,
               'show_friends': True}

    # Check if request is POST
    if request.method == 'POST':
        # If it is, cancel the request
        friend_request.delete()
        friend_list.requested_friends.remove(friend_request.recipient)

    # Render friend page
    return render(request, 'base/friends.html', context)


# Function to accept or decline a friend request
@login_required
def accept_friend_request(request, friend_request_id):
    # Define user
    user = request.user

    # Get invitations
    invitations = Invitation.objects.filter(
        recipient=user, accepted=False).exclude(sender=request.user)

    # Get events
    events = Event.objects.filter(
        Q(organizer=user) | Q(attending_guests=user)).distinct()

    # Get incoming friend requests
    received_friends_requests = FriendRequest.objects.filter(
        recipient=user, accepted=False)

    # Get outgoing friend requests
    sent_friend_requests = FriendRequest.objects.filter(sender=user)

    # Get friend list
    friend_list = FriendList.objects.get(user=user)

    # Define received and sent requests, and friends
    received_requests = received_friends_requests.all()
    sent_requests = sent_friend_requests.all()
    friends = friend_list.friends.all()

    # Get friend request to accept or decline
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)

    # Define sender and receipient, as well as their friend lists
    sender = friend_request.sender
    recipient = friend_request.recipient
    sender_friend_list, _ = FriendList.objects.get_or_create(user=sender)
    recipient_friend_list, _ = FriendList.objects.get_or_create(user=recipient)

    # Create context of all relevant user and friend info
    context = {'invitations': invitations,
               'events': events, 'friends': friends, 'received_requests': received_requests, 'sent_requests': sent_requests,
               'show_create_event_form': False,
               'show_edit_event_form': False,
               'show_view_event': False,
               'show_friends': True}

    # Check if request is POST
    if request.method == 'POST':
        # Get accept or decline
        action = request.POST.get('action')

        # Check if accepted
        if action == 'accept':
            friend_request.accepted = True
            friend_request.delete()
            if sender_friend_list:
                sender_friend_list.friends.add(recipient)
            if recipient_friend_list:
                recipient_friend_list.friends.add(sender)

            return render(request, 'base/friends.html', context)

        # Check if declined
        elif action == 'decline':
            friend_request.accepted = False
            friend_request.delete()
            if sender_friend_list:
                sender_friend_list.requested_friends.remove(recipient)

            return render(request, 'base/friends.html', context)
