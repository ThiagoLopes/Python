from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @hybrid_property
    def nice_name(self):
        return str(self.name).upper()

    def __repr__(self):
        return str(self.name)


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    full_adress = column_property(street_name + ' ' + street_number)
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

    def __repr__(self):
        return str(self.full_adress)
