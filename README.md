# Locate followers

## Description
This program is a web-app that creates a map with locations of twitter
followers of a user marked on the map.

## Usage
``` python
import main.py
```
The app will run auttomatically. You need to click on a link to the server.
The web-page with a form will appear. Fill in the fileds with valid twitter
username and bearer token and press the "Find locations" button or press enter.
If all the arguments are correct, the map will be displayed. If you did not
fill in some fields, the page with a failure message will be displayed.

## Example of running
Example of generated web-page:

![Output](/images/img1.png?raw=true "output")

Example of the map if @elonmusk is entered as a username:

![Output](/images/img2.png?raw=true "output")

Example of a failure message page:

![Output](/images/img3.png?raw=true "output")

## Results
The result of running a program is a web application. It takes twitter username
and bearer token from the user and displays a map with locations of the users
one follows. The popups of the markers contain information on the username of
the person in that location.

## License
[MIT](https://github.com/linvieson/twitter-api/blob/main/LICENSE.txt)
