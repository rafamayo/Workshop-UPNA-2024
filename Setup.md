# JPA HAPI FHIR server with a supported database
  + This is the best option when creating a server from scratch and when the FHIR resources are appropriate out of the box
  + Here is a list of the supported databases: https://hapifhir.io/hapi-fhir/docs/server_jpa/database_support.html
  + The database should be created but left empty
  + The schema, the tables as well as taking care of all the FHIR stuff is done by the FHIR server
  + This is the easier version, but we have no control of the database schema

## Vitual Machine
+ Linux Container (LXC) running Ubuntu 22.04

## Install HAPI FHIR jpa-server-starter
+ https://github.com/hapifhir/hapi-fhir-jpaserver-starter
+ Checked out the project into ~/opt/project
+ Installed openjdk version 21
+ `sudo apt install openjdk-21-jre-headless`
+ `sudo apt-get install openjdk-17-jdk openjdk-17-demo openjdk-17-doc openjdk-17-jre-headless openjdk-17-source`
+ Installed Apache maven build tool
  + Version? Description?

## Check the installation
+ Change into the HAPI FHIR server project
+ `cd ~/project/hapi-fhir-jpaserver-starter`
+ Run using jetty: `mvn -Pjetty jetty:run`
+ It works! The server is accessibe at http://localhost:8080

## Change the database to postgreSQL

### Install postgreSQL
1. Install PostgreSQL
+ Use the script here: https://www.postgresql.org/download/linux/ubuntu/
```
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

2. Configure postgreSQL
+ Only the local user `postgres` can access the application postgres and manage the databases.
+ We want to configure the `postgres` user
  + In a terminal, type: `sudo -u postgres psql postgres`
  + this connects as a role with same name as the local user, i.e. `postgres`, to the database called `postgres` (1st argument to psql).
  + Set a password for the "postgres" database role using the command: `\password postgres`
  + and give your password when prompted. The password text will be hidden from the console for security purposes.
  + Type Control+D or \q to exit the posgreSQL prompt.

Configuration:
```
user: postgres
password: somepass
```

+ Now we want to turn our linux user into a postgres user with superuser privileges to be able to create and manage databases.
 ```
 sudo -u postgres createuser --superuser $USER
 sudo -u postgres psql

 postgres=# \password $USER
```
  + In the command `\password` replace `$USER` with your linux user.

  + Now your linux user is also a postgres user with superuser privileges and can create a new database `$ createdb mydb`

### Create a database to use with the FHIR server
`$ createdb fhir_server`


## Install dbeaver
+ **We will use dbeaver to directly inspect the database used by the FHIR Serversomepass**
+ www.dbeaver.io
+ Download Debian package `dbeaver-ce_23.3.2_amd64.deb`
+ `sudo dpkg -i ./dbeaver-ce_23.3.0_amd64.deb`
+ The proper driver for the database engine is required: PostgreSQL JDBC Driver

## Install PostgreSQL JDBC Driver
+ https://jdbc.postgresql.org
+ `postgresql-42.7.1.jar`
+ Moved the driver to `~/opt/jdbc`

## Connect dBeaver to a PostgreSQL database
+ Inspired by following video: + https://www.youtube.com/watch?v=zYhv1Dj8Gmw
+ Database/New Database connection
+ Select PostgreSQL
+ Host: localhost
+ Database: fhir_server
+ Userame: someuser
+ Password: somepass
+ In driver Settings go to Libraries and add the jdbc driver for postgreSQL from `~/opt/jdbc`
+ In the tab PostgreSQL check "show all databases" and "show template databases"
+ In the tab Main click on test connection


## Configure the HAPI FHIR server to use postgreSQL 
To configure the starter app to use PostgreSQL, instead of the default H2, update the application.yaml file.
The file is here: `~/project/hapi-fhir/src/main/resources`

Modify as follows:
```
spring:
  datasource:
    url: 'jdbc:postgresql://localhost:5432/fhir_server'
    username: someuser
    password: somepass
    driverClassName: org.postgresql.Driver
  jpa:
    properties:
      hibernate.dialect: ca.uhn.fhir.jpa.model.dialect.HapiFhirPostgres94Dialect
      hibernate.search.enabled: false

      # Then comment all hibernate.search.backend.*
```
+ You need to specify the database you want to use. In our case `fhir_server`
+ You need to specify username and password to access this database

## Run locally using jetty
+ Change into the project folder `cd ~/project/hapi-fhir-jpaserver-starter`
+ Use the following command: `mvn -Pjetty jetty:run`
+ It shoud work and the server can be accessed at `http://localhost:8080`
+ If you now inspect the database `fhir_server` using dbeaver, you will see that it has content (tables have been created, etc.)

## Install a REST client
+ Installed insomnia https://insomnia.rest/download
  + Documentation: https://docs.insomnia.rest/
+ Installed advanced REST client https://github.com/advanced-rest-client/arc-electron/releases
  + Documentation: https://docs.advancedrestclient.com/ 

## Use a REST client to create your first resource
+ Let's create our first `Patient` resource.
+ Execute a POST request on the URL `http://localhost:8080/fhir/Patient`
+ with headers `Content-Type: application/fhir+json`
+ and the following content in the request body:

```
{
    "resourceType" : "Patient",
    "name":[
    {
        "use" : "usual",
        "text" : "Mike Wheeler",
        "family" : "Wheeler",
        "given" : ["Mike"]
    },
    {
        "use" : "nickname",
        "text" : "Dungeon Master"
    }
    ],
    "gender": "male",
    "birthDate": "1971-04-07"
}
```
+ Since the database was completely empty, this was the very first resource created and it thus gets the resource `id = 1`.
+ You can see this on the request response using the REST client.
+ You can also execute a GET request on the url `http://localhost:8080/fhir/Patient`


## Where to find information about the FHIR resources in the database?
+ The contents of the database `fhir_server` have been created by the HAPI FHIR Server application
+ Documentation of the database schema: https://hapifhir.io/hapi-fhir/docs/server_jpa/schema.html
  + HFJ_RESOURCE: Resource Master Table

## Using dbeaver to run a query on the database
+ https://dbeaver.com/2022/04/14/your-first-queries-in-the-sql-editor/
+ Open the SQL Editor: `SQL Editor/Open SQL console`
+ The master table is `hfj_resource`
  + `select * from hfj_resource where res_type = 'Patient'`
  
![Running a query using dbeaver](https://github.com/rafamayo/Workshop-UPNA-2024/blob/main/assets/sql_query_hfj_resource.png?raw=true)

  + There is one row (there is just one resource in the database) containing *administrative* information about the resource. The most important columns are:
    + res_id
    + res_type
    + res_ver
    + res_version
+ The complete *raw* information about a resource is contained in the table `hfj_res_ver`
+ To find the information corresponding to our newly created resource, we use the `res_id` from the table `hfj_resource`
+ `select * from hfj_res_ver where res_id = 1`

![alt text](https://github.com/rafamayo/Workshop-UPNA-2024/blob/main/assets/sql_query_hfj_res_ver.png?raw=true)

+ Every resource has a many rows as versions (versions are created when the resource is updated)
+ The *raw* information is in one of the columns `rest_text` or `res_text_vc`


## Deploy using tomcat

Because the integration tests within the project rely on the default H2 database configuration, it is important to either explicitly skip the integration tests during the build process, i.e., mvn install -DskipTests, or delete the tests altogether. Failure to skip or delete the tests once you've configured PostgreSQL for the datasource.driver, datasource.url, and hibernate.dialect as outlined above will result in build errors and compilation failure.
