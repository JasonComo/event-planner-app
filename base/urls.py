from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accept_invitation/<int:invitation_id>/',
         views.accept_invitation, name='accept_invitation'),
    path('accept_friend_request/<int:friend_request_id>/',
         views.accept_friend_request, name='accept_friend_request'),
    path('create_event/', views.create_event, name='create_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/',
         views.delete_event, name='delete_event'),
    path('leave_event/<int:event_id>/',
         views.leave_event, name='leave_event'),
    path('view_event/<int:event_id>/', views.view_event, name='view_event'),
    path('send_message/<int:event_id>/',
         views.send_message, name='send_message'),
    path('friends/', views.view_friends, name='view_friends'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:friend_id>/',
         views.remove_friend, name='remove_friend'),
    path('cancel_friend_request/<int:friend_request_id>/',
         views.cancel_friend_request, name='cancel_friend_request')
]
