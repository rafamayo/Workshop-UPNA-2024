# Version 3: adding references

A powerful concept in FHIR are references. References allow to link resources to other resources thus creating a network which models a clinical scenario. Using references makes it possible to perform reverse searches.

## Adding references

In our scenario every patient needs a practitioner. We will expand the process of creating a new patient by requiring the selection of a treating practioner.

We need to update the view function `ǹew_patient()` in the route `/new_patient` to handle displaying and selecting practitioners:

```python
@app.route('/new_patient', methods=['GET', 'POST'])
def new_patient():

    # Fetch practitioners to populate the dropdown
    practitioners_query = practitioner.Practitioner.where({})
    practitioners = practitioners_query.perform_resources(smart.server)
    practitioner_list = [{'id': prac.id, 'name': f"{prac.name[0].given[0]} {prac.name[0].family}"} for prac in practitioners if prac.name]

    if request.method == 'POST':
        # Logic to create the new patient
        new_patient = patient.Patient({
            'name': [{
                'use': 'official',
                'family': request.form['last_name'],
                'given': [request.form['given_name']],
            }],
            'gender': request.form['gender'],
            'birthDate': request.form['birth_date'],
            'address': [{
                'line': [request.form['postcode'] + ' ' + request.form['city'] + ' ' + request.form['country']],
                'city': request.form['city'],
                'postalCode': request.form['postcode'],
                'country': request.form['country']
            }]
        })

        # Assuming the selection of a practitioner is optional, include it if provided
        practitioner_id = request.form.get('practitioner_id')
        if practitioner_id:
            # Create a FHIRReference for the generalPractitioner
            gp_reference = FHIRReference({
                'reference': f"Practitioner/{practitioner_id}"
            })
            new_patient.generalPractitioner = [gp_reference]

        # Attempt to create the Patient on the FHIR server
        try:
            result = new_patient.create(smart.server)
            if result:
                patient_id = new_patient.id  # Capture the ID of the created patient
                message = f'Patient successfully created with ID: {patient_id}'
        except Exception as e:
            message = f"An error occurred: {str(e)}"
        
        #return redirect(url_for('index'))  # Redirect to the index page after creation
        return render_template('new_patient.html', message=message, practitioners=practitioner_list)
    
    
    return render_template('new_patient.html', practitioners=practitioner_list)
```
1. Fetch practitioners for a drop-down list: 
    - When the route is accessed, regardless of the method, it first queries a list of practitioners from the FHIR server. 
    - It uses `practitioner.Practitioner.where({})` to get all available practitioners (since it's passed an empty filter, implying no specific query conditions).
    - The fetched practitioners are then processed into a list of dictionaries (`practitioner_list`), each containing a practitioner's `id` and `name` (constructed from their given name and family name). This list is intended for populating a dropdown menu in the HTML form on the `new_patient` page.

2. Handle POST Request (Form Submission):
    - If the method of the request is POST (the form on the `new_patient.html` page has been submitted), the code enters the conditional block to process the form data.
    - A new `Patient` object is created with details taken from the form inputs, such as the patient's name, gender, date of birth, and address.
    - If a practitioner is selected in the form (identified by `practitioner_id`), this is added to the new patient's data as their `generalPractitioner` (**a FHIRReference**).
    - The code attempts to create a new patient on the FHIR server using `new_patient.create(smart.server)`. If successful, the unique ID of the newly created patient (`new_patient.id`) is captured.

3. Success or Error Handling:
    - If the patient is successfully created, a success message including the new patient's ID is prepared.
    - If there is an exception (e.g., network issues, validation errors from the FHIR server, etc.), an error message is prepared instead.

4. Rendering the Response:
    - If a POST request was made and processed (whether successful or with errors), the `new_patient.html` template is rendered again, this time with the `message` (indicating success or error) and the `practitioners_list` (for the dropdown).
    - If the request was a GET (meaning the user has just navigated to the `/new_patient` URL without submitting the form), the `new_patient.html` template is rendered with just the `practitioners_list` for the dropdown, without any message (since no action has been performed yet).

5. Template Rendering:
    - `return render_template('new_patient.html', practitioners=practitioner_list)` returns the HTML content generated from the `new_patient.html` template, using the given context variables (such as `practitioners_list` and possibly `message`).
  
> [!NOTE]
> We need to import FHIRReference `from fhirclient.models.fhirreference import FHIRReference
`

The template `new_patient.html` needs to be modified to include a drop-down list with the available practitioners:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create New Patient</title>
</head>
<body>
    <h1>Create New Patient</h1>
    <form method="post" action="/new_patient">
        <input type="text" name="given_name" placeholder="Given Name" required><br>
        <input type="text" name="last_name" placeholder="Last Name" required><br>
        <input type="date" name="birth_date" placeholder="Date of Birth" required><br>
        <select name="gender" required>
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="unknown">Unknown</option>
        </select><br>
        <input type="text" name="postcode" placeholder="Postcode" required><br>
        <input type="text" name="city" placeholder="City" required><br>
        <input type="text" name="country" placeholder="Country" required><br>
        <select name="practitioner_id" required>
            <option value="">Select Practitioner</option>
            {% for prac in practitioners %}
                <option value="{{ prac.id }}">{{ prac.name }}</option>
            {% endfor %}
        </select><br>
        <input type="submit" value="Create Patient">
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
The template now includes a drop-down list for selecting a practitioner.

+ Inside the form, there's a dropdown menu created with a `<select>` element for choosing a practitioner. The options for this dropdown are dynamically generated using a Jinja2 for loop, which iterates over the `practitioners` variable passed from the Flask view. Each practitioner's ID and name are used to populate the value and display text of each `<option>`.

## Exercise: make Practitioner a requirement

1. Modify the code of `new_patient()` to require selecting a practitioner before creating a new patient: it should not be possible to create a new patient if no practitioner has been selected.
