## Scenario 1: Use the JPA HAPI FHIR server with a supported database
  + This is the best option when creating a server from scratch and when the FHIR resources are appropriate out of the box
  + Here is a list of the supported databases: https://hapifhir.io/hapi-fhir/docs/server_jpa/database_support.html
  + The database should be created but left empty
  + The schema, the tables as well as taking care of all the FHIR stuff is done by the FHIR server
  + This is the easier version, but we have no control of the database schema
  + This option is described here: https://www.youtube.com/watch?v=5ypS1XJm4YE

## Install PostgresQL 16.1

### Steps
1. Install PostgreSQL
+ Use the script here: https://www.postgresql.org/download/linux/ubuntu/
```
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

2. Set up postgresql
+ https://help.ubuntu.com/community/PostgreSQL

To start off, we need to set the password of the PostgreSQL user (role) called "postgres"; we will not be able to access the server externally otherwise. As the local “postgres” Linux user, we are allowed to connect and manipulate the server using the psql command.

In a terminal, type:
`sudo -u postgres psql postgres`
this connects as a role with same name as the local user, i.e. "postgres", to the database called "postgres" (1st argument to psql).

Set a password for the "postgres" database role using the command:
`\password postgres`
and give your password when prompted. The password text will be hidden from the console for security purposes.
Type Control+D or \q to exit the posgreSQL prompt.

```
user: postgres
password: somepass
```

### Alternative Server Setup

If you don't intend to connect to the database from other machines, this alternative setup may be simpler.

By default in Ubuntu, Postgresql is configured to use 'ident sameuser' authentication for any connections from the same machine. Check out the excellent Postgresql documentation for more information, but essentially this means that if your Ubuntu username is 'foo' and you add 'foo' as a Postgresql user then you can connect to the database without requiring a password.

Since the only user who can connect to a fresh install is the postgres user, here is how to create yourself a database account (which is in this case also a database superuser) with the same name as your login name and then create a password for the user:

 ```
 sudo -u postgres createuser --superuser $USER
 sudo -u postgres psql

 postgres=# \password $USER
```
In the command `\password` replace `$USER` with your linux user.

Now your linux user is also a postgres user with superuser privileges and can create a new database

`$ createdb mydb`

Client programs, by default, connect to the local host using your Ubuntu login name and expect to find a database with that name too. So to make things REALLY easy, use your new superuser privileges granted above to create a database with the same name as your login name:
```
 sudo -u postgres createdb $USER
```
Connecting to your own database to try out some SQL should now be as easy as:
```
 psql
```
Creating additional database is just as easy, so for example, after running this:
```
 create database amarokdb;
```
You can go right ahead and tell Amarok to use postgresql to store its music catalog. The database name would be amarokdb, the username would be your own login name, and you don't even need a password thanks to 'ident sameuser' so you can leave that blank. 


## Install OpenJDK
+ Java is required for dbeaver and for the HAPI FHIR Server
+ Version 21 (latest LTS version)
+ `sudo apt install openjdk-21-jr-headless`
+ `sudo apt-get install openjdk-17-jdk openjdk-17-demo openjdk-17-doc openjdk-17-jre-headless openjdk-17-source`


## Install DBeaver
+ www.dbeaver.io
+ Download Debian package `dbeaver-ce_23.3.0_amd64.deb`
+ `sudo dpkg -i ./dbeaver-ce_23.3.0_amd64.deb`
+ The proper driver for the database engine is required: PostgreSQL JDBC Driver


## Install PostgreSQL JDBC Driver
+ https://jdbc.postgresql.org
+ `postgresql-42.7.1.jar`
+ Moved the driver to `/opt/jdbc`

  
## Connect dBeaver to a PostgreSQL database
+ https://www.youtube.com/watch?v=zYhv1Dj8Gmw
+ How to create and configure a new connection to a PostgreSQL database


## Create a new database using dbeaver

![alt text](https://github.com/rafamayo/Workshop-UPNA-2024/blob/main/Create_new_db_dbeaver_1.png?raw=true)

![alt text](https://github.com/rafamayo/Workshop-UPNA-2024/blob/main/Create_new_db_dbeaver_2.png?raw=true)

![alt text](https://github.com/rafamayo/Workshop-UPNA-2024/blob/main/Create_new_db_dbeaver_3.png?raw=true)


## Install Apache Tomcat on Ubuntu

+ Apache Tomcat is a Java web application server.. It provides a *pure Java* HTTP web server environment in which Java code can also run.
+ https://tomcat.apache.org/
+ Version 10.1.17
+ https://linuxize.com/post/how-to-install-tomcat-10-on-ubuntu-22-04/

+ Didn't add the system user. Just performed a very simple installation
+ Download the current version
+ Extracted into `~/opt/tomcat/apache-tomcat-10.1.17`
+ Created a symbolic link `sudo ln -s ~/opt/tomcat/apache-tomcat-10.1.17 ~/opt/tomcat/latest`
+ Make the scripts inside the tomcat `bin` folder executable: `sudo chmod +x ~/opt/tomcat/latest/bin/*.sh`
+ To start the server run `~/opt/tomcat/latest/bin/startup.sh`
+ To shutdown the servr run `~/opt/tomcat/latest/bin/shutdown.sh`
+ The server can be reached at `http://localhost:8080`


## Install the HAPI FHIR Server
+ Download the Zip-file (latest version) from `https://github.com/hapifhir/hapi-fhir-jpaserver-starter`
+ Extracted into `~/opt/hapi-fhir-jpaserver-starter`


## Install the Spring Tools Suite
+ https://youtu.be/U3C8tTxYa7k?feature=shared
+ Download from https://spring.io/tools/
+ Copy into ~/opt/
+ Extract
+ Execute the file `SpringToolSuite4`
+ Configure the spring tools as described im the video  https://www.youtube.com/watch?v=5ypS1XJm4YE


## Import the HAPI FHIR Server project into VS Code
Figure
Figure

Install the recommended JAVA extension packs

+ Modify the datasource in src/resources/application.yaml
  + Lines 17 - 20
  + database: fhir_server
  + user: somebody
  + password: somepass

+ Line 186 tester:
