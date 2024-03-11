from flask import Flask, render_template, request, redirect, url_for
from fhirclient import client

app = Flask(__name__)

# Default FHIR server settings
settings = {
    'app_id': 'my_web_app',
    'api_base': 'http://127.0.0.1:8080/fhir/' # The default FHIR server runs on the localhost
#    'api_base': 'https://fhir.server/baseDstu3/' # A public test server
}
smart = client.FHIRClient(settings=settings)

@app.route('/')
def index():
    return render_template('index.html', title='FHIR Server')

@app.route('/new_practitioner')
def new_practitioner():
    return render_template('new_practitioner.html')

@app.route('/new_patient')
def new_patient():
    return render_template('new_patient.html')

@app.route('/search')
def search():
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
