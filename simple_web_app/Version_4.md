# Version 4: performing searches with references

References in FHIR are unidirectional:
+ the patient has a reference to her practitioner (having the patient, you can find out who the practitioner is),
+ but the practitioner has no references to her patients.
+ This has performance reasons: a practitioner will typically treat several patients and the treated patients could potentially be added and removed often. Using unidirectional references means, that when adding a new patient, the practitioner does not need to be updated, only a reference in the newly created patient is necessary.
+ Similar scenarios are references from `Observation` to `Subject` (which could be a `Patient`) or from a `Condition` (a problem or diagnosis) to `Subject` (which could also be a `Patient`) 

To find the patients associated with a specific paractitioner, we need to search with references. The URL of the correponding HTTP request would be like this:

```http
GET {{FHIR_URL}}/Patient?general-practitioner=Practitioner/<practitioner id>
```
where `practitioner_id` is the id of the practitioner for whom we want to get the patients.

If we don't have the id, but have thepractitioner's name, then we can use a chained search:

```http
GET {{FHIR_URL}}/Patient?general-practitioner:Practitioner.name=<practitioner name>
```

For our web app we use the methods of the `fhirclient` library. We need to modifiy the `search()` view function: for each practitioner found, we will perform another search to find Patients where the `generalPractitioner` reference matches the Practitioner's ID.

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
        
        practitioners_to_patients = {}
        search_result = []
        
        # Perform search based on resource type
        if resource_type == 'Practitioner':
            search_result = practitioner.Practitioner.where(search_params).perform_resources(smart.server)
            # For each practitioner found, find related patients
            for prac in search_result:
                prac_id = prac.id
                # Search for patients with the current practitioner as their generalPractitioner
                patient_search_result = patient.Patient.where({'general-practitioner': f'Practitioner/{prac_id}'}).perform_resources(smart.server)
                
                # This is a dictionary where: each key is a Practitioner object (resulting from the FHIR search) and
                # each corresponding value is a list of Patient objects that reference the respective Practitioner.
                practitioners_to_patients[prac] = patient_search_result
            # Render a template with both practitioners and related patients
            return render_template('search_results.html', practitioners_to_patients=practitioners_to_patients, resource_type=resource_type)
        else:  # Default to Patient search
            search_result = patient.Patient.where(search_params).perform_resources(smart.server)
            # Render a template with search results for patients only
            return render_template('search_results.html', search_results=search_result, resource_type=resource_type)

    # If the request method is not POST, just render the search form page
    return render_template('search.html')
```

1. Search for Practitioners: If the `resource_type` is `'Practitioner'`, the function performs the search and then, for each Practitioner found, searches for Patients referring to this Practitioner as their `generalPractitioner`.

2. Mapping Practitioners to Patients: A new dictionary `practitioners_to_patients` maps each Practitioner object to a list of Patients. This allows the template to iterate through each Practitioner and their corresponding Patients.

3. Template Rendering: Depending on whether the search is for Practitioners or Patients, the function renders `search_results.html` with different data: either the `practitioners_to_patients` mapping (for Practitioners) or the `search_results` list (for Patients).

The template `search_results.html` needs to be adjusted accordingly to handle the new structure, especially for displaying Patients related to each Practitioner when the `resource_type` is `'Practitioner'`. This involves adding nested loops to iterate through each Practitioner and then through their associated Patients within the template.

```html
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
</head>
<body>
    <h1>Search Results for {{ resource_type }}</h1>
    <!-- Rendering Practitioners together with their Patients if any -->
    {% if resource_type == 'Practitioner' %}
        {% if practitioners_to_patients %}
            <ul>    
            {% for practitioner, patients in practitioners_to_patients.items() %}
                <li>
                    <strong>Practitioner:</strong> {{ practitioner.name[0].given[0] }} {{ practitioner.name[0].family }}</h2>
                    {% if patients %}
                        <ul>
                        {% for patient in patients %}
                            <li>
                                Name: {{ patient.name[0].given[0] }} {{ patient.name[0].family }}
                                {% if patient.birthDate %}
                                    - Date of Birth: {{ patient.birthDate | fhirdate }}
                                {% endif %}
                                {% if patient.gender %}
                                    - Gender: {{ patient.gender }}
                                {% endif %}
                                {% if patient.address %}
                                    - Address: {{ patient.address[0].country }}, {{ patient.address[0].city }}, {{ patient.address[0].postalCode }}
                                {% endif %}
                            </li>  
                        {% endfor %}
                        </ul>
                    {% else %}
                        <ul><li>No patients associated.</li></ul>
                    {% endif %}
                </li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No results found.</p>
        {% endif %}
    {% else %}
        <!-- Rendering Patients -->
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
    {% endif %}
    <a href="/search">Back to Search</a>
</body>
</html>
```

> [!NOTE]
> Privacy considerations: is it a good idea just listing all patients being treated by a practitioner?
> The formatting of the results could be improved in different ways. This is left as an exercise!

## Exercise (challenging!)
1. Patients will usually have a condition (a clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern). Can you modify the code so that when creating a new patient a condition can be entered?
  + You should use the resource `Condition` (https://hl7.org/fhir/condition.html)
  + The resource `Condition` has a reference to the subject (the patient)
  + Conditions should be coded using publicly defined code systems such as LOINC or SNOMED CT. Here is an example: https://hl7.org/fhir/condition-example-f203-sepsis.html
  + To do this you should have a repository of conditions on your server (possibly entered beforehand)
