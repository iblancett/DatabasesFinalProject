# Object-Relational Mapping
Isa Blancett
iblancett@olin.edu

The code used was adapted from the SQLAlchemy Tutorial.
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

## What is ORM?
Definition of ORM

## Overview
Why do we use ORM?

### Structural Differences

### Creating (Saving)

### Reading

### One-to-Many Relationships

## SQLAlchemy

### Connecting
:
```

```

### Mapping Declaration
The first two steps to using an ORM are to define our database tables and our own classes to be mapped to the tables.  SQLAlchemy allows these two steps to be done in parallel.  These feature of SQLAlchemy is known as the "Declarative" system.  To use this system, we define our class in terms of a base class, known as the declarative base class.  We can create a class "Pet" with this base class, which maps to the table 'pets', as defined in the variable '__tablename__'.  At minimum, the class needs to contain the '__tablename__' attribute and at least one Column.
Our class will contain six Columns: the type, name, age, breed, and organization of the pet.

```
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    pet_type = Column(String(50))
    name = Column(String(50))
    age = Column(Integer)
    breed = Column(String(50))
    organization = Column(String(50))
```

### Metadata
Via the Declarative system, we have created table metada, which is stored in the Table object, a member of a registry known as MetaData.  MetaData can emits schema generation commands to our database, such as CREATE TABLE statements.  to create our pets table (and other tables if desired), we can call the create_all() method.  To create and connect to an in-memory-only SQLite Database, we establish an engine which can then be passed through the metadata method.

```
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
```

This will generate something that looks like this:

```
CREATE TABLE pets (
	id INTEGER NOT NULL, 
	pet_type VARCHAR(50), 
	name VARCHAR(50), 
	age INTEGER, 
	breed VARCHAR(50), 
	organization VARCHAR(50), 
	PRIMARY KEY (id)
)
```

### Instance of Mapped Class
Next, I will create an instance of my pet, Gala, just as I would with a typical Python class.  We can print some of Gala's attributes and take note that her ID is a None value, by default.  This will change once we create a session and start talking to our database.

```
gala = Pet(pet_type='Dog', name='Gala', age=12, breed='Laborador Retriever', organization='Blancett Bungalow')
print(gala.name)
print(gala.age)
print(str(gala.id))
```

```
Gala
12
None
```

### Sessions
When using SQLAlchemy, Sessions establish conversations with the database.

```
# Create a Session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

# Initiate Session
session = Session()
```

### Performing Operations
Since we have already created our Pet object, Gala, we can add her to the database using the add method.
```
session.add(gala)
```

Now that the object is added, let's try to pull it from the database.  To do this, we create query object using the Pet class.

