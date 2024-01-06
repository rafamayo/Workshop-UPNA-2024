## Scenario 1: Use the JPA HAPI FHIR server with a supported database
  + This is the best option when creating a server from scratch and when the FHIR resources are appropriate out of the box
  + Here is a list of the supported databases: https://hapifhir.io/hapi-fhir/docs/server_jpa/database_support.html
  + The database should be created but left empty
  + The schema, the tables as well as taking care of all the FHIR stuff is done by the FHIR server
  + This is the easier version, but we have no control of the database schema
  + This option is described here: https://www.youtube.com/watch?v=5ypS1XJm4YE
