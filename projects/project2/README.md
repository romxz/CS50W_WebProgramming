# Project 2: Flack

## Web Programming with Python and JavaScript

## Objectives

Build simple online messaging service using Flask. Users create or select an existing channel, and are able to send and receive messages with one another in real time. Gain practice with:

* Server-side JavaScript
* Building web user interfaces
* Socket.IO for client-server communication


## Core Features


* **Login:** Users register/login with a unique username.
* **Channel Creation:** Users can create new channels.
* **Channel List:** Users can see a list of all current channels, and selecting them to view the channel.
* **Messages View:** Inside a channel, users can see any messages in that channel. App stores certain amount of recent messages per channel in server-side memory.
* **Sending Messages:** Inside a channel, users can send text messages. All users in the channel can see the new message *(with username and timestamp)*. Sending and receiving messages does not require reloading the page.

WIP:
* **Remembering the Channel:** If a user is on a channel page, closes the web browser window, and then goes back to the web app, the app remembers what channel the user was on previously and takes the user back to that channel.
* **Extra functionality:** Supporting deleting one's own messages, user attachments (e.g. file uploads) as messages, private messaging between two users

## Installation

Go to the `project2/` root folder, then install via pip:

```
pip3 install -r requirements.txt
```


You can run the (development) server via:
```
flask run
```


Current setup is for `sqlite`. 

Project uses dotenv for convenience, so make sure to include public environment variables in `.flaskenv`, and private environment variables in `.env`.
Do make sure to include a `SECRET_KEY` envorinment variable, e.g. inside `project2/.env` (untracked), so that `os.getenv('SECRET_KEY')` can then access it.
