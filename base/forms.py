from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Invitation, User

from django import forms
from .models import Event, FriendList


# Form to create an event
class EventForm(forms.ModelForm):
    invited_guests = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    attending_guests = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Initially an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }
        ),
        initial='2023-11-13'
    )

    class Meta:
        model = Event
        fields = ['title', 'location', 'date',
                  'description', 'invited_guests', 'attending_guests']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        # Handles editing an event
        edit_mode = kwargs.pop('edit_mode', False)
        super(EventForm, self).__init__(*args, **kwargs)

        # Invitable guests are all friends
        if user:
            user_friend_list, created = FriendList.objects.get_or_create(
                user=user)
            friends = user_friend_list.friends.all()
            self.fields['invited_guests'].queryset = friends

            # If edit mode, include attending guests as well
            if edit_mode:
                event = kwargs['instance']
                accepted_guests = event.attending_guests.all()
                self.fields['attending_guests'].queryset = accepted_guests

# Form to register a user


class UserRegistrationForm(UserCreationForm):

    username = forms.CharField()

    password1 = forms.CharField(widget=forms.PasswordInput)

    password2 = forms.CharField(widget=forms.PasswordInput)

    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2']

# Form to add a friend


class AddFriendForm(forms.Form):
    username = forms.CharField()
