# Horadrim Software
A basic database management system

## How to run?

Run these commands:

pip install bplustree

python3 src/horadrimSoftware.py inputFileName outputFileName

## Commands

Type the commands into the input file

There are two types of commands: DDL commands and DML commands.

### DDL Commands

#### Creating a Table
 Format: create type {type_name} {number_of_fields} {primary_key_index} {field_1_name} {field_1_type} ........ {field_n_name} {field_n_type}
 
 Example: create type human 6 1 name str age int height int weight int occupation str favourite_meal str

To be continued...
