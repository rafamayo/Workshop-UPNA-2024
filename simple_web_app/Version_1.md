# Version 1: simple web app skeleton

## Functionality
+ There is an `index.html` page rendering four buttons.
+ Each of these four buttons leads to a different HTML page:
  + **FHIR server:** allows to specify which server to use
  + **Search:** allows to search for existing patients and practitioners in the server (no functionality in this version)
  + **New practitioner:** allows to create a new practitioner (no functionality in this version)
  + **New patient:** allows to create a new patient (no functionality in this version)

In the project folder we will need to create the folowing:
  + A subfolder `static`: containing style information (will be empty for now)
  + A subfolder `templates`: containing all required HTML files
  + A file `main.py`: this is the main file which will be executed to run the web app

The file `main.py` must contain the following:
1. Import statements for `Flask` and `fhirclient`.
2. Initialization of the Flask app.
3. A route for the index.html page that renders the page with the title "FHIR Server" and the four specified buttons.
4. Placeholder routes for the buttons "New Practitioner", "New Patient", "Search", and "Server", each leading to a different HTML page.
5. Starting the Flask app.

## Executing the web app
In the project folder run the command `python main.py`. The web app can be reached at: `http://127.0.0.1:5000`

## How does `index.html` work?
When we want to see one of the pages, i.e. `New practitioner`, we press the button `New practitioner` and the corresponding reference is followed, i.e. `/new_practitioner`

This results in calling the function defined under the corresponding `route` in `main.py`. In this case, the route would be `@app.route('/new_practitioner')` and the function is:

```python
@app.route('/new_practitioner')
def new_practitioner():
    return render_template('new_practitioner.html')
```

the result of which is to render the HTML page `new_practitioner.html`.

> [!NOTE]
> This is achieved by sending an HTTP request of type GET to the running Flask server. For each of the HTML pages that we want rendered, we need a similar route which executes a GET request.


## Getting user input and changing the default server with `server.html`
The application uses per default a public FHIR test server. If we want to change the used server, we press the button `Server` to display the HTML page `server.html` where we can enter the new server URL.

Displaying the page `server.html` corresponds to a `GET` request just as explained before:
+ There is a `route` named `/server` in `main.py` which results in `return render_template('server.html' ...)`

There are however some differences:
+ The code line for rendering the HTML page is now `return render_template('server.html', server_url=smart.server.base_uri)`
+ In this line the current `base_uri` of the server is passed as an argument in `server_url` when rendering the page
+ The HTML page `server.html` contains a form for accepting user input and within this form there is an input element of type `text` with name `server_url`.

```html
<input type="text" id="server_url" name="server_url" value="{{ server_url }}"><br>
```
> [!NOTE]
> This is the element used to input the server URL. When rendering the page, the current value will be shown first.

+ The form contains an element of type `submit` shown as the button `Update Server`. When pressing this button, the specified server URL should be sent to our web app to update the value of the current server URI. This corresponds to a POST request: we post some information to the server.

+ In the HTML page `server.html` the form has an associated `post` method that results in calling the route `/server` in the `main.py` file.

```html
<form method="post" action="/server">
  <label for="server_url">FHIR Server URL:</label><br>
  <input type="text" id="server_url" name="server_url" value="{{ server_url }}"><br>
  <input type="submit" value="Update Server">
  <!-- Cancel button to return to the index page -->
  <a href="/"><button type="button">Cancel</button></a>
</form>
```

+ In `main.py` the route needs to support the `GET` and `POST` methods.
  + The `GET` method will be used to render the page `server.html` with the current value of the server's base URI
  + The `POST` method is used to accept input from the user and perform the corresponding actions, in this case update the current value of the FHIR server's base URI. The results of the `POST` are returned to the web app in the `request` object. We need to access the request object to get the contents of the form, e.i. the user input.

```python
@app.route('/server', methods=['GET', 'POST'])
def server_info():
    if request.method == 'POST':
        # Update FHIR server URL based on user input
        new_server_url = request.form['server_url']
        global smart
        smart = client.FHIRClient(settings={'app_id': 'my_web_app', 'api_base': new_server_url})
        return redirect(url_for('index'))
    else:
        return render_template('server.html', server_url=smart.server.base_uri)
```

> [!NOTE]
> This is basically the way we will implement the interaction with our application: there is a route for every HTML page and each route will have to support the `GET` and `POST` methods to either display the page or accept user input. When accepting input from the user this will in turn result in interacting with the FHIR server.

> [!TIP]
> In order to use your local FHIR server, you need to enter it like this: `http://localhost:8080/fhir/` or `127.0.0.1:8080/fhir/`
