# This code is adapted from the SQLAlchemy Tutorial
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html

import subprocess
import json

# Connecting
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Declare a Mapping
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

    def __repr__(self):
        return "<Pet(name='%s', type='%s', age=%d, breed='%s')>" % (
                             self.name, self.pet_type, self.age, self.breed)

# Create a Schema
Base.metadata.create_all(engine)

# Create an Instance of Mapped Class
gala = Pet(pet_type='Dog', name='Gala', age=12, breed='Laborador Retriever')
print(gala.name)
print(gala.age)
print(str(gala.id))

# Create a Session
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

# Initiate Session
session = Session()

# Add Object
session.add(gala)
my_dog = session.query(Pet).filter_by(name='Gala').first()
print(gala is my_dog)

# Add More Pets
session.add_all([Pet(pet_type='Cat', name='Hermes', age=6, breed='Maine Coon'), Pet(pet_type='Dog', name='Floki', age=8, breed='Chihuahua'), Pet(pet_type='Cat', name='Roo', age=5, breed='Tabby'), Pet(pet_type='Dog', name='Willow', age=1, breed='Miniature Poodle')])

# Update Info
gala.age = 13
session.dirty
session.new
session.commit()
print(gala.id)



# Building a Relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    owner = Column(String, nullable=False)
    pet_id = Column(Integer, ForeignKey('pets.id'))
    pet = relationship("Pet", back_populates="owners")

    def __repr__(self):
        return "<Owner(owner='%s')>" % self.owner

Pet.owners = relationship("Owner", order_by=Owner.id, back_populates="pet")

Base.metadata.create_all(engine)

# Working with Related Objects
piper = Pet(pet_type='Dog', name='Piper', age=10, breed='Border Collie')
print(piper.owners)

piper.owners = [Owner(owner='Molly Blancett'), Owner(owner='Joan Blancett')]
print(piper.owners[1])
print(piper.owners[1].pet)

session.add(piper)
session.commit()
piper = session.query(Pet).filter_by(name='Piper').first()
print(piper)
print(piper.owners)
