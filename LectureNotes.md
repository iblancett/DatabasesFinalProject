# Object-Relational Mapping
Isa Blancett
iblancett@olin.edu

The code used was adapted from the SQLAlchemy Tutorial.
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

## What is ORM?
Definition of ORM

## SQLAlchemy Implementation

### Mapping Declaration
The first two steps to using an ORM are to define our database tables and our own classes to be mapped to the tables.  SQLAlchemy allows these two steps to be done in parallel.  These feature of SQLAlchemy is known as the "Declarative" system.  To use this system, we define our class in terms of a base class, known as the declarative base class.  We can create a class "Pet" with this base class, which maps to the table 'pets', as defined in the variable '__tablename__'.  At minimum, the class needs to contain the '__tablename__' attribute and at least one Column.
Our class will contain six Columns: the type, name, age, and breed of the pet.

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
	PRIMARY KEY (id)
)
```

### Instance of Mapped Class
Next, I will create an instance of my pet, Gala, just as I would with a typical Python class.  We can print some of Gala's attributes and take note that her ID is a None value, by default.  This will change once we create a session and start talking to our database.

```
gala = Pet(pet_type='Dog', name='Gala', age=12, breed='Laborador Retriever')
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

We can also add some more pets using the add_all method.
```
session.add_all([Pet(pet_type='Cat', name='Hermes', age=6, breed='Maine Coon'), Pet(pet_type='Dog', name='Floki', age=8, breed='Chihuahua'), Pet(pet_type='Cat', name='Roo', age=5, breed='Tabby'), Pet(pet_type='Dog', name='Willow', age=1, breed='Miniature Poodle')])
```

Let's say Gala just turned 13.  We'd want to update the database to reflect this.  We can simply reassign a value to her age attribute.  The session listens in and knows that new objects have been added and that Gala's age is changed.  We can go ahead and commit these changes.

```
gala.age = 13
session.dirty
session.new
session.commit()
print(gala.id)
```

In return, we receive a list of SQL operations that were performed on the database.
```
2019-09-07 18:53:45,154 INFO sqlalchemy.engine.base.Engine UPDATE pets SET age=? WHERE pets.id = ?
2019-09-07 18:53:45,154 INFO sqlalchemy.engine.base.Engine (13, 1)
2019-09-07 18:53:45,155 INFO sqlalchemy.engine.base.Engine INSERT INTO pets (pet_type, name, age, breed) VALUES (?, ?, ?, ?, ?)
2019-09-07 18:53:45,155 INFO sqlalchemy.engine.base.Engine ('Dog', 'Piper', 10, 'Border Collie', 'Blancett Dogs')
2019-09-07 18:53:45,155 INFO sqlalchemy.engine.base.Engine INSERT INTO pets (pet_type, name, age, breed) VALUES (?, ?, ?, ?, ?)
2019-09-07 18:53:45,155 INFO sqlalchemy.engine.base.Engine ('Dog', 'Floki', 8, 'Chihuahua', 'Claire Care')
2019-09-07 18:53:45,155 INFO sqlalchemy.engine.base.Engine INSERT INTO pets (pet_type, name, age, breed) VALUES (?, ?, ?, ?, ?)
2019-09-07 18:53:45,155 INFO sqlalchemy.engine.base.Engine ('Cat', 'Roo', 5, 'Tabby', 'Claire Care')
2019-09-07 18:53:45,156 INFO sqlalchemy.engine.base.Engine INSERT INTO pets (pet_type, name, age, breed) VALUES (?, ?, ?, ?, ?)
2019-09-07 18:53:45,156 INFO sqlalchemy.engine.base.Engine ('Dog', 'Willow', 1, 'Miniature Poodle', 'Rogers Ranch')
2019-09-07 18:53:45,156 INFO sqlalchemy.engine.base.Engine COMMIT
```
Also, ids have now been assigned to our objects, which can be checked by calling `print(gala.id)`.

### Relationships
Now that we have created one table in our database, we can create another to build a relationship.  To do this, let's create a new class called Owners which will store the names of the pet's owners.  We can restrict the values of the pet_id to be only one of the existing pets, by using the ForeignKey Construct.

We will also use the relationship() construct to inform the ORM that the owner class should be linked to the Pet class.  This creates a many-to-one relationship as discussed in the previous slide.  We also must remember to create the table using the create_all method.

```
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    owner = Column(String, nullable=False)
    pet_id = Column(Integer, ForeignKey('pets.id'))
    pet = relationship("Pet", back_populates="owners")

Pet.owners = relationship("Owner", order_by=Owner.id, back_populates="pet")

Base.metadata.create_all(engine)
```
The last step is to give a pet some owners.  We'll use another dog in my family, Piper, in this example.  We start this by simply creating an instance of the Pet class.

```
piper = Pet(pet_type='Dog', name='Piper', age=10, breed='Border Collie')
```

If we check the value of Piper's owners, we find that the attribute is empty.  We can populate it with the following:
```
piper.owners = [Owner(owner='Molly Blancett'), Owner(owner='Joan Blancett')]
```

Now, we can check if the owners and the pet have been linked.
```
print(piper.owners[1])
print(piper.owners[1].pet)
```

These commands show that, yes, the owners now have a relationship with their pet.
```
<Owner(owner='Joan Blancett')>
<Pet(name='Piper', type='Dog', age=10, breed='Border Collie')>
```

