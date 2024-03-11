from flask import Flask, render_template, request, redirect, url_for
from fhirclient import client
import fhirclient.models.practitioner as practitioner
import fhirclient.models.patient as patient

app = Flask(__name__)

# Default FHIR server settings
settings = {
    'app_id': 'my_web_app',
    'api_base': 'http://127.0.0.1:8080/fhir/' # The default FHIR server runs on the localhost
#    'api_base': 'https://fhir.server/baseDstu3/' # A public test server
}
smart = client.FHIRClient(settings=settings)

# A jinja2 filter to format fhirdate objects
@app.template_filter('fhirdate')
def fhirdate_filter(date):
    if date is not None and hasattr(date, 'date'):
#        return date.date.isoformat()    # ISO format YYYY-MM-DD
        return date.date.strftime('%d/%m/%Y')   # Format DD/MM/YYYY
    return 'Unknown'

app.jinja_env.filters['fhirdate'] = fhirdate_filter

@app.route('/')
def index():
    return render_template('index.html', title='FHIR Server')

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


@app.route('/new_patient', methods=['GET', 'POST'])
def new_patient():

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

        # Attempt to create the Patient on the FHIR server
        try:
            result = new_patient.create(smart.server)
            if result:
                patient_id = new_patient.id  # Capture the ID of the created patient
                message = f'Patient successfully created with ID: {patient_id}'
        except Exception as e:
            message = f"An error occurred: {str(e)}"
        
        #return redirect(url_for('index'))  # Redirect to the index page after creation
        return render_template('new_patient.html', message=message)
    
    return render_template('new_patient.html')


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

# Start the application
if __name__ == '__main__':
    app.run(debug=True)
