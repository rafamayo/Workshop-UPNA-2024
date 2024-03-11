# Project versions for the workshop

## Version 1: basic structure

In the project directory
Directory `static`: contains style information
Directory `templates`: includes the required `html` files
File `main.py`: the main file which will be executed to run the web app

The `main.py` must contain the following:
1. Import statements for Flask and fhirclient.
2. Initialization of the Flask app.
3. A route for the index.html page that renders the page with the title "FHIR Server" and the four buttons you specified.
4. Placeholder routes for the buttons "New Practitioner", "New Patient", "Search", and "Server", each leading to a different HTML page.
5. Starting the Flask app.