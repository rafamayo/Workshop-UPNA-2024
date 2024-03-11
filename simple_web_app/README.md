# A simple clinical web application

We create a simple clinical web application using python and flask to interact with the FHIR server.

## Basic Requirements
+ Specify the base url of the FHIR server to connect to
+ Get a list of Patients
+ Get a list of Practitioners
+ Search for a specific patient using some criteria
+ Search for a specific practitioner using some criteria
+ Create a new Practitioner
  + Specifiy the following data: last name, given name, birthdate, gender postcode, city, country
+ Create a new Patient
  + Specifiy the following data: last name, given name, birthdate, gender postcode, city, country
  + Specify the general parctitioner (introduce the concept of references)

## Advanced features
+ In the paractitioner results list, we want to be able to select one practitioner and ask for the patients she is treating.
  + Introduce the concept of searching with references
+ In the patients results list, we want to be able to select a patient and enter a condition
  + Introduce the concept of terminology 

## Bonus
+ We'll make the application look nicer using some material design elements


# Use case for the web app

# What is Flask?

Flask is a lightweight WSGI (Web Server Gateway Interface) web application framework written in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It was developed by Armin Ronacher as part of the Pocoo projects collection.

**How Does Flask Work?**

Flask operates as a web server that listens for requests from web clients (such as browsers), processes them according to the logic defined by the developer, and then sends responses back to the clients. Here’s a brief overview of how Flask works:

1. **Routing**: Flask allows you to map specific URLs to Python functions. These mappings tell Flask what code to execute for different web page requests. This is known as routing. When a request is received, Flask checks the URL and invokes the associated function.

2. **View Functions**: The functions linked to routes are known as view functions. These functions return responses, which can be HTML templates, JSON data, a redirect, a file, or any other content. Flask provides mechanisms to render templates, making it easy to return HTML pages.

3. **Development Server**: Flask comes with a built-in development server, which simplifies the process of testing your web applications locally. The development server can be started with a simple command and automatically reloads your application when changes are detected.

4. **Extensions and Configuration**: While Flask is designed to be lightweight and simple, it can be easily extended with “Flask Extensions” to add additional functionalities like database integration, authentication mechanisms, and form validation. Flask can also be configured to adapt to different environments, making it flexible for both development and production.

5. **Request and Response Objects**: Flask provides request and response objects that encapsulate the details of HTTP requests and responses. In your Flask application, you can access data sent by clients (such as form data and query parameters) through the request object, and you can customize the data you send back (such as setting cookies or status codes) using the response object.

6. **Templates**: Flask integrates with the Jinja2 templating engine, which allows for the dynamic generation of HTML pages. Templates separate the presentation layer from the business logic, allowing developers to change the appearance of web pages without altering the underlying Python code.

7. **Contexts**: Flask uses contexts to temporarily make certain objects globally accessible. For example, during a request, the request object can be accessed anywhere in your code. Contexts simplify the handling of request-related data.


# Prerequisites for the simple web app

## Packages in python
+ The programming language python is used for many different applications an many different packages exist to support these applications
+ To be able to use packages, we need to install them first
+ Python has its own package manager known as `pip`
+ If not already available, we need to install it `sudo apt install python3-pip`
+ Now we can install all necessary python packages

## Environments in python
+ Possibly there is already a python installation in your system.
+ When developing applications, it might be necessary to install and use packages sometimes with specific versions and dependencies
+ When working on several projects, each of these projects might require different packages with different versions and dependencies
+ If we are not careful, the different projects will interfere with each other
+ A solution to this problem is to use environments
+ For each project a different environment is set up
+ Before starting to work in a project, the corresponding environment is activated
+ This way all changes done will apply only to the active environment
+ When finished working on a project, the environment should be deactivated

### Install venv
+ The first step is to install venv on your system `sudo apt install python3.10-venv`

### Create a virtual environment
+ Change into the project directory
+ Create the virtual environment using `python -m venv venv`
+ The second argument is the location to create the virtual environment
+ You should exclude your virtual environment directory from your version control system using .gitignore or similar.

### Activate the virtual environment
+ Change into the project directory
+ Activate the virtual environment every time you need to work on the project, install new packages or run the project
+ `source venv/bin/activate`

### Deactivate the virtual environment
+ When done working on the project, you need to deactivate the virtual environment
+ `deactivate`

### After finishing development
+ The vitual environment still needs to be activated every time the application is to be run

## Flask and fhirclient
+ Flask needs to be installed on the system: `pip install Flask`
+ To interact with the FHIR server we will use the `fhirclient` python client. The correspondig package needs to be installed: `pip install fhirclient` 



**References**

+ https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
+ https://www.darioz.ch/posts/venv-and-git/venv-and-git/
