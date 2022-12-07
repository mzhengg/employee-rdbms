# Employee Database Management System

Data modeling is an important job of a Data Engineer. So, in this project, I designed a RDBMS (Relational Database Management System) for employee management applications to practice this skill.

*Technologies:*
* MySQL
* Docker

## Database Principles

A brief overview of important database concepts.

### 1) Overview
Data modeling is the process of creating a visual representation of either a whole information system or parts of it to communicate connections between data points and structures.  

Goal is to illustrate types of data used and stored, relationships among these data types, and the ways the data can be grouped and organized and its formats and attributes.  

Data models built around business needs. Rules and requirements defined upfront through feedback from business stakeholders so they can be incorporated into the design of a new system or adapted into an existing one.  

*Benefits of data modeling:*
* Provides project scope
* Acts as documentation
* Improves performance
* Reduces data and application errors  

*Types of data models (hierarchy):*
* Conceptual data models:
    * Establish the entities and their relationships
* Logical data models
    * Define the attributes and elaborate on their relationships
        * Ex. Entity Relationship diagram (ERD), Key-Based model (KB), Fully-Attributed model (FA)
* Physical data models
    * Describes the database-specific implementation of the data model

*Data modeling process:*
* Identify the entities of business importance
* Identify key attributes of each entity
* Identify relationships among entities
* Map attributes to entities completely
* Assign keys as needed and decide on a degree of normalization (that balances the need to reduce redundancy with performance requirements)
* Finalize and validate the data model

### 2) Relational Databases

Relational Database: a type of database that stores and provides access to data points that are related to one another 

RDBMS: The software used to store, manage, query, and retrieve data stored in a relational database  

Data Integrity: having correct data in database (no repeating or incorrect values and broken relationships)
* Entity integrity:  each row of a table has a unique and non-null primary key
* Referential integrity: each value in the foreign key must have a matching value in the primary key or it must be null
* Domain integrity: all data values in each column must be valid (proper data type and length)

Relationships: associations between entities (tables)
* One-to-one: a record in one table has a connection to a single record in another table
* One-to-many: a record in one table has connections to multiple records in another table
* Many-to-many: multiple records in one table have connections with multiple records in another table (incompatible with relational databases)

Parent tables: contain the primary key.  

Child tables: contain the foreign key
* A child table always points back at the parent table.  

Look-up table: a table that has two columns: "key" and "value". The keys are usually integers or short string codes. The keys are being used by other tables. Thus, we can quickly search data because the lookup keys are connected to all the corresponding rows.  

Cardinality: the maximum number of times a row in one table can relate to the rows in another table  

Modality: the minimum number of times a row in one table can relate to the rows in another table

### 3) Schemas
Structured data: made up of well-defined data types with patterns that make them easily searchable  

Unstructured data: made up of files in various formats, such as videos, photos, texts, audio, and more  

Data engineers collect unstructured data, transform it into structured data, and store it in database management systems (DBMS) to make it available for analysis  

A schema is a collection of database objects  

There are a variety of ways to arrange schema objects in the schema models designed for data warehousing:
* Star Schema: (the simplest)
    * Design: contains a fact table at the center connected to a number of associated dimensional tables
        * Fact table: contains all the primary keys of the dimensional tables and stores quantitative information for analysis
        * Dimensional tables: provide descriptive information for all the quantitative information in the fact table (thus dimensional tables are relatively smaller than fact tables). Commonly used dimensions: people, products, place, and time

![alt text](https://upload.wikimedia.org/wikipedia/commons/b/bb/Star-schema.png)

* Snowflake Schema: (variant of Star Schema)
    * Design: contains a fact table at the center connected to a number of associated dimensional tables that have their own sub-dimensional tables

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Snowflake-schema.png/1200px-Snowflake-schema.png)

* Galaxy Schema:
    * Design: contains two fact tables that share dimensional tables between them and have their own dimensional tables

![alt text](https://streamsets.b-cdn.net/wp-content/uploads/Galaxy-Schema.png)

### 4) Keys

Natural key: a set of attributes that already exist in the table that can be used to make keys (see below)  

Surrogate key: a system generated attribute with no business meaning that can be used to make keys (see below)  

Super key: a set of attributes (can include unnecessary attributes) that can uniquely identify each row in a table (there can be many Super keys in a table)

* Candidate key: a subset of Super keys devoid of any unnecessary attributes that are not important for uniquely identifying each row in a table (there can be many Candidate keys in a table)

    * Primary key: Out of all the Candidate keys, we pick the one that has a minimal, non-null set of attributes that can uniquely identify each row in a table (there can only be one Primary key in a table)

    * Alternate key: Any of the remaining Candidate keys

Foreign key: an attribute that is a Primary key in its parent table, but is included as an attribute in the child table to generate a relationship between them (each value in the foreign key must correspond to a value in the primary key otherwise it should be null)  

Simple key: a key made up of one column  

Composite key: a key made up of two or more columns  

Compound key: a key made up of two or more foreign keys from different tables  

### 5) Normalization

Partial dependency: when a non-key column in a table is not dependent on the entire primary key  

Functional dependency: when a non-key column in a table is dependent on the entire primary key  

Transitive dependency: when a column is dependent on another column through a dependency (A -> C because A -> B where B -> C) and causes a FD  

Normalization: the process by which data in a relational database is organized to eliminate data redundancy by removing all model structures that provide multiple ways to know the same fact

* First Normal Form:
    * All column values are atomic
* Second Normal Form:
    * It is in 1NF
    * No partial dependencies, otherwise the column(s) should be moved to another table
* Third Normal Form:
    * It is in 2NF
    * No transitive dependencies, otherwise the column(s) should be moved to another table  

Denormalization: the process of adding precomputed redundant data to an otherwise normalized relational database to improve read performance of the database

### 6) Index

Non-clustered index: list of indices where each index points to all the corresponding rows  

Clustered index: list of indices where each index points to a block containing all the corresponding rows (actually reorganizes the data)  

## Data Model

I used an ER (entity relationship) diagram to build a logical model for the relational database.  

![alt text](https://miro.medium.com/max/1168/1*QkIeA-uwU244QoG0jF3FBg.png)

## How the Database Works

The database was created in MySQL and saved as a .sql file, called 'database.sql',  in ./containers/warehouse/. It was containerized with a docker-compose.yml file in order to isolate the database from the local system and ensure reproducibility on other systems as long as they have Docker installed.  

The database is stored in the container named *warehouse*.  

A MySQL base *image* (mysql:5.7) was used to build the container. 

*restart* was defined to 'always' to ensure the container continuously runs.  

Several important MySQL parameters were passed into the container from environmental variables defined in the .env file of this repository. The .env file is a hidden file that defines environmental variables that can be used by the scripts in this repo. For the purposes of this project, the MYSQL_USER and MYSQL_PASSWORD were set to 'admin' and the MYSQL_ROOT_PASSWORD was set to 'root'. Please note that the passwords that were used are not secure and in a real-life application, stronger passwords should be used to increase security.  

The MYSQL_DATABASE is set to 'WAREHOUSE', which is consistent with the schema defined in the 'database.sql' file. It is important that the schema, or database, is the same or the database will not be succesfully built.  

*ports* is used to specifify the host port and container port (host:container) so that a connection can be established to this container from within and without. When container ports are mentioned in docker-compose.yml, they will be shared amongst services started by that docker-compose because they are on the same network.  

*volumes* provides the path to the 'database.sql' file so that the database can be imported into the container.  
