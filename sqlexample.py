from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    breed = Column(String)
    organization = Column(String)
    house_trained = column(Integer)

    def __repr__(self):
        return "<User(name='%s', age=%d, breed='%s', organization='%s')>" % (
                             self.name, self.age, self.breed, self.organization)
