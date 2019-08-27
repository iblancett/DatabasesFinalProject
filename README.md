# PetFinder Database with SQLAlchemy
Final Project for Databases SP19 at Olin College

SQL Alchemy Introduction

Background:
Python Library
Interface to relational databases such as
Oracle
DB2
MySQL
PostgresSQL
SQLite
Purpose: ability to map python objects to tables without significantly changing code/format

Example of lower-level python interfaces (DB-API):
```
sql = ”INSERT INTO user(user_name, password) VALUES (%s,%s)”
cursor = conn.cursor()
cursor.execute(sql, (‘gala’, ‘labrador’))
```

Problems:
unnecessary amount of code
prone to errors
string manipulation makes app vulnerable to injection attacks
generating explicit string makes migration to different database difficult

Example of the same instructions for Oracle DB-API:
```
sql = ”INSERT INTO user(user_name, password) VALUES (:1, :2)”
cursor = conn.cursor()
cursor.execute(sql, ‘gala’, ‘labrador’)
```

With SQLAlchemy SQL expression language:
statement = user_table.insert(user_name=’gala’, password=’labrador’)
statement.execute()

Pros of SQL:
- Write queries with a Pythonic expression builder
```
statement = user_table.select(and_(
    user_table.c.created >= date(2015,1,1),
    user_table.c.created <   date(2016,1,1)),
result = statement.execute()
```

- Provides an ORM to automatically populate databases as Python objects change

Object-relational impedance match = set of difficulties experienced when objects or class definitions need to be mapped to a relational model

Differences:
- Data Type - relational prohibits by-reference objects, scalars and operators can have differences in semantics
- Structure - relational models are defined usually with global, unnamed variables which don’t necessarily translate, ex. OO allows for objects composed of other objects


