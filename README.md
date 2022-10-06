# Horadrim Software
A simple database management system

## How to run?

Run these commands:

pip install bplustree

python3 src/horadrimSoftware.py inputFileName outputFileName

## Commands

Type the commands into the input file

There are two types of commands: DDL commands and DML commands.

### DDL (Data Definition Language) Commands

#### Creating a Table
 Format: create type {type_name} {number_of_fields} {primary_key_index} {field_1_name} {field_1_type} ........ {field_n_name} {field_n_type}
 
 Example: create type human 6 1 name str age int height int weight int occupation str favourite_meal str
#### Listing Existing Tables
 Format: list type
 
#### Deleting a Table
 Format: delete type {table_name}
 
 ### DML (Data Manipulation Language) Commands
 
 #### Create Records
 
 Format: create record {table_name} {field_1_value} ...... {field_n_value}
 
 #### Delete Record
 
 Format: delete record {table_name} {primary_key}
 
#### Search Record

Format: search record {table_name} {primary_key}
 
#### Filter Records

Format: filter record {table_name} {condition}

Condition format: {primary key} {logical operation} {value} 
 
#### Update Record

Format: update record {table_name} {primary_key} {field_1_value} ...... {field_n_value}

#### List Records

Format: list record {table_name}

## Note
As intended, data is stored in disk, therefore if user creates some records and doesn't delete them, they will appear on next runs.
Join operations, multiple users, authentication/authorization mechanisms, encryption aren't implemented for sake of simplicity
