### A Django event planner with CRUD capabilities. Users can signup and create, edit, and delete events, as well as maintain a friend list.


## Description
This project was created in Python's Django framework. It allows users to plan and keep track of their own/friends' events. The application has CRUD capabilities, and supports user registration/login, as well as friend list functionality.

Key features:
- Signup/Login/Logout: Allows users to register for an account with a username, first and last name, and password. 
- Event Creation/Deletion: Users can create an event with a title, location, date, time, and description. They can also invite guests from their friend list. In addition, they can delete their own event.
- Event Editing/: Users can completely modify their own event, including the list of invitees and attending guests.
- Chat Capability: Each event has a group chat, where all attending users can communicate with one another.
- Friend List Management: Users can add and remove friends, as well as cancel pending friend requests.
  
## Installation
You should use a virtual environment to prevent conflicts. Make sure it is installed on your machine.
```
pip install virtualenv
```

Clone the the repository.
```
git clone https://github.com/JasonComo/event-planner.git
```

Navigate to the repository.
```
cd event-planner
```

Open your terminal, and create a virutal environment.
```
virtualenv env
```

Activate the virtual environment on Windows:
```
.\env\Scripts\Activate.ps1
```

Activate the virtual environment on Mac/Linux:
```
virtualenv env
```
Install the project dependencies.
```
pip install -r requirements.txt
```

## Usage
After installation, run the server.
```
python manage.py runserver
```
### Register
Click the "Register" button to create an account.

### Login
After creating an account, click the "Login" button and login by entering your username and password. 

### Event Functions
Create an event by clicking the "Create Event" button. You can input the title, location, date, time, and description. In addition, you can select friends to invite. An event can also be deleted or edited by clicking "Edit Event" or "Delete Event." Users can also chat with one another using the chat box on the right side. If you are not the organizer, you can leave the event by clicking "Leave Event"

### Friends
Add a friend by clicking the "Friends" button and typing in the username of the friend you want to add. You can also cancel outgoing requests, or remove friends.

### View Event
View an event by clicking on the event under the "Events" tab on the left side.




