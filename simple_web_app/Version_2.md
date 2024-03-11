# Version 2: adding functionality

Now we want to implement the following functionality:
+ It shall be possible to create a new Practitioner with the following data:
  + Last Name, given Name, date of Birth, gender, postcode, city, country
+ It shall be possible to create a new Patient with the following data:
  + Last Name, given Name, date of Birth, gender, postcode, city, country
+ It shall be possible to search for patients and practitioners in the FHIR server

## Creating a new Practitioner

We need a file `new_practitioner.html` containing a form to enter the required data.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create New Practitioner</title>
</head>
<body>
    <h1>Create New Practitioner</h1>
    <form method="post" action="/new_practitioner">
        <input type="text" name="last_name" placeholder="Last Name" required><br>
        <input type="text" name="given_name" placeholder="Given Name" required><br>
        <input type="date" name="birth_date" placeholder="Date of Birth" required><br>
        <select name="gender" required>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="unknown">Unknown</option>
        </select><br>
        <input type="text" name="postcode" placeholder="Postcode" required><br>
        <input type="text" name="city" placeholder="City" required><br>
        <input type="text" name="country" placeholder="Country" required><br>
        <input type="submit" value="Create Practitioner">
        <!-- Cancel button to return to the index page -->
        <a href="/"><button type="button">Cancel</button></a>
    </form>
    <!-- Display the message if it exists -->
    {% if message %}
        <div>{{ message }}</div>
    {% endif %}
</body>
</html>
```
The form includes several text input fields and a select input field for the gender which corresponds to a drop-down list. The date input element is shown by most browsers as a calendar object.

The form is associated to a `POST` method that results in calling the route `/new_practitioner` in the `main.py` file.

In the file `main.py` we need to implement the route `/new_practitioner` with support for the methods `GET` and `POST`. `GET` displays the HTML page, while `POST` handles the information coming from the form. 

```python
@app.route('/new_practitioner', methods=['GET', 'POST'])
def create_practitioner():
    message = None  # Initialize message variable
    practitioner_id = None  # Initialize practitioner ID variable
    
    if request.method == 'POST':
        # Convert the birthdate string from the form into the correct format
        birth_date_str = request.form['birth_date']
        
        # Construct Practitioner resource
        prac = practitioner.Practitioner({
            'name': [{
                'use': 'official',
                'family': request.form['last_name'],
                'given': [request.form['given_name']],
            }],
            'gender': request.form['gender'],
            'birthDate': birth_date_str,
            'address': [{
                'line': [],
                'city': request.form['city'],
                'postalCode': request.form['postcode'],
                'country': request.form['country']
            }]
        })
        
        # Attempt to create the Practitioner on the FHIR server
        try:
            result = prac.create(smart.server)
            if result:
                practitioner_id = prac.id  # Capture the ID of the created practitioner
                message = f'Practitioner successfully created with ID: {practitioner_id}'
        except Exception as e:
            message = f"An error occurred: {str(e)}"
    
    # Render the same template whether a POST request was successful or not
    return render_template('new_practitioner.html', message=message, practitioner_id=practitioner_id)
```

When the form is submitted (`POST` method), a new `Practitioner` resource is constructed using the form data. The information coming from the form is returned inside the `request` object.

```python
  # Construct Practitioner resource
  prac = practitioner.Practitioner({
    'name': [{
      'use': 'official',
      'family': request.form['last_name'],
      'given': [request.form['given_name']],
    }],
    'gender': request.form['gender'],
    'birthDate': request.form['birth_date'],  # Directly use the string from form
    'address': [{
      'line': [],
      'city': request.form['city'],
      'postalCode': request.form['postcode'],
      'country': request.form['country']
    }]
  })
```
We use the implementation of the `Practitioner` resource in the module `fhirclient`. We will need to consult the documentation of the Practitioner resource at https://hl7.org/fhir/resourcelist.html as well as the documentation of the module `fhirclient` at https://docs.smarthealthit.org/client-py/

> [!TIP]
> The project page, including a flask web app can be found here: https://github.com/smart-on-fhir/client-py

> [!WARNING]
> For the code to work, we need to import the required classes `import fhirclient.models.practitioner as practitioner`

After constructing the resource, the `.create()` method attempts to create the Practitioner on the FHIR server. 

```python
    try:
        result = prac.create(smart.server)
        if result
            practitioner_id = prac.id  # Capture the ID of the created practitioner
            message = f'Practitioner successfully created with ID: {practitioner_id}'
    except Exception as e:
        message = f"An error occurred: {str(e)}"
```
If successful, a correponding message is displayed and the user stays on the new_practitioner page in case further practioners are to be created. 

## Exercise: Creating a new Patient

1. Creating a new patient is a similar process:
  + a file `new_patient.html` containig a form for data input is required. The form must be associated to a POST method and the route must be specified
  + The file `main.py` needs to be modified to contain a route `/new_patient` which handles the `GET` and `POST` methods
  + The GET method displays the page and the POST method handles the form data by constructing a `Patient` resource and attempting to create it on the server 
  + The import statement `import fhirclient.models.patient as patient` is required


## Searching for patients and practitioners

We want to get a list of the patients or practitioners available in the server. We want to be able to specifiy some criteria for the search. 

Create `search.html` including a form with dropdowns and input fields for the user to select between "Practitioner" or "Patient" and to enter search parameters such as "Last Name", "Given Name", "Date of Birth", "Gender", "Postcode", "City", and "Country". It will also include a "Search" button to submit the form.

The form is associated to a `POST` method which results is calling the route `/search`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Search</title>
</head>
<body>
    <h1>Search for Practitioner or Patient</h1>
    <form method="post" action="/search">
        <select name="resource_type">
            <option value="Practitioner">Practitioner</option>
            <option value="Patient">Patient</option>
        </select><br>
        <input type="text" name="last_name" placeholder="Last Name"><br>
        <input type="text" name="given_name" placeholder="Given Name"><br>
        <input type="date" name="birth_date" placeholder="Date of Birth"><br>
        <select name="gender">
            <option value="">Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="unknown">Unknown</option>
        </select><br>
        <input type="text" name="postcode" placeholder="Postcode"><br>
        <input type="text" name="city" placeholder="City"><br>
        <input type="text" name="country" placeholder="Country"><br>
        <input type="submit" value="Search">
        <!-- Cancel button to return to the index page -->
        <a href="/"><button type="button">Cancel</button></a>
    </form>
</body>
</html>
```

The file `main.py`, needs to be updated to implement a view function `search()` in the route `/search` which handles the search form submission. This involves capturing the form data, constructing the search query based on the entered parameters, performing the search against the FHIR server, and then ideally displaying the results.

```python
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        resource_type = request.form['resource_type']
        search_params = {
            'family': request.form.get('last_name', ''),
            'given': request.form.get('given_name', ''),
            'birthdate': request.form.get('birth_date', ''),
            'gender': request.form.get('gender', ''),
            'address-postalcode': request.form.get('postcode', ''),
            'address-city': request.form.get('city', ''),
            'address-country': request.form.get('country', '')
        }
        
        # Filter out empty search parameters
        search_params = {k: v for k, v in search_params.items() if v}
        
        # Perform search based on resource type
        if resource_type == 'Practitioner':
            search_result = practitioner.Practitioner.where(search_params).perform_resources(smart.server)
        else:  # Default to Patient search
            search_result = patient.Patient.where(search_params).perform_resources(smart.server)
        
        # Render a template with search results
        return render_template('search_results.html', search_results=search_result, resource_type=resource_type)

    # if the request method is not POST (is ist GET?), just render the page
    return render_template('search.html')
```
First if the request method is a POST, the form data is captured:
+ The data is returned in the request object
+ A dictionary `search_params` (a series of key-value pairs) is created to contain the form data

```python
    if request.method == 'POST':
        resource_type = request.form['resource_type']
        search_params = {
            'family': request.form.get('last_name', ''),
            'given': request.form.get('given_name', ''),
            'birthdate': request.form.get('birth_date', ''),
            'gender': request.form.get('gender', ''),
            'address-postalcode': request.form.get('postcode', ''),
            'address-city': request.form.get('city', ''),
            'address-country': request.form.get('country', '')
        }
```
Next, empty key-value pairs are filtered out from the dictionary `search_params`

```python
search_params = {k: v for k, v in search_params.items() if v}
```

Finally, the type of FHIR resource `resource_type` is checked (`Practitioner` or `Patient`), a corresponding query, based on the provided search parameters (`search_params`), is constructed and the query is executed against a FHIR server. The result (`search_result`) will be a list of resources from the FHIR server that match the criteria specified by the user. 

```python
        if resource_type == 'Practitioner':
            search_result = practitioner.Practitioner.where(search_params).perform_resources(smart.server)
        else:  # Default to Patient search
            search_result = patient.Patient.where(search_params).perform_resources(smart.server)
```
The results are then rendered using an additional template (HTML page)

```python
    return render_template('search_results.html', search_results=search_result, resource_type=resource_type)
```

If the request method is not a POST (in our case it defaults to a GET), then the page `search.html` is just rendered

```python
    return render_template('search.html')
```

> [!NOTE]
> We need an additional template `search_results.html` to display the search results.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
</head>
<body>
    <h1>Search Results for {{ resource_type }}</h1>
    {% if search_results %}
        <ul>
        {% for result in search_results %}
            <li>
                Name: {{ result.name[0].given[0] }} {{ result.name[0].family }}
                {% if result.birthDate %}
                - Date of Birth: {{ result.birthDate | fhirdate }}
                {% endif %}
                {% if result.gender %}
                - Gender: {{ result.gender }}
                {% endif %}
                {% if result.address %}
                - Address: {{ result.address[0].country }}, {{ result.address[0].city }}, {{ result.address[0].postalCode }}
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No results found.</p>
    {% endif %}
    <a href="/search">Back to Search</a>
</body>
</html>
```

This code represents an HTML template to display search results using the Jinja2 templating engine

+ `{{ resource_type }}`: Inside the `<h1>` tag, this Jinja2 template syntax is used to inject the type of resources being searched for (e.g., 'Practitioner' or 'Patient') into the title of the page, making it "Search Results for [Resource Type]".

+ Conditionally displaying search results
  + `{% if search_results %}`: A Jinja2 control structure that checks if there are any search results to display. If `search_results` is not empty, the code inside this block is executed.
  + `{% else %}`: Part of the conditional that specifies what should be displayed if there are no search results (i.e., `search_results` is empty or undefined).

+ Iterating over search results
  + `{% for result in search_results %}`: Another Jinja2 control structure that loops over each item in `search_results`. For each item (which represents a FHIR resource), it generates an HTML list item (`<li>`) containing details of that resource.
  + Inside the loop, various attributes of each search result are displayed, such as name, date of birth, gender, and address. These are accessed using Jinja2's template syntax, e.g., `{{ result.name[0].given[0] }}` **(assuming the resource has a name with a 'given' part, remember that humans may have several names!)**.
  + `{% if %}` statements inside the loop are used to check if certain information (like birthDate, gender, address) is available before trying to display it.

+ Filters and data formatting
  + `{{ result.birthDate | fhirdate }}`: This applies a custom Jinja2 filter `fhirdate`, which formats the FHIR date object into a human-readable date string. The `fhirdate` custom filter is defined in the Flask application to convert FHIR date formats to standard date formats.

+ Navigation link
  + `<a href="/search">Back to Search</a>`: Provides a hyperlink that allows the user to return to the search page or form. This improves navigation within the application by allowing users to easily initiate a new search.

+ No results fallback
  + `<p>No results found.</p>`: This paragraph is displayed if there are no search results, providing clear feedback to the user.

