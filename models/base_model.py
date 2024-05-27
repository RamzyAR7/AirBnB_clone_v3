#!/usr/bin/python3
"""
this module for base class
"""
from os import getenv
from datetime import datetime
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, DateTime, Column
import models

if getenv('HBNB_TYPE_STORAGE') == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """BaseModel class the parant for others"""

    def __init__(self, *args, **kwargs):
        """ init methoud for BaseModel"""
        self.id = None
        self.created_at = None
        self.updated_at = None
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    if getenv('HBNB_TYPE_STORAGE') == "db":
        id = Column(String(60), unique=True, nullable=False, primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow())
        updated_at = Column(DateTime, default=datetime.utcnow())

    def __str__(self):
        """ str reprecentation """
        return "[{}] ({}) {}".format(type(self).__name__,
                                     self.id, self.__dict__)

    def save(self):
        """ to save obj in json file """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, command="DEL"):
        """ to convert obj"""
        dct = self.__dict__.copy()
        dct['__class__'] = type(self).__name__
        dct['created_at'] = self.created_at.isoformat()
        dct['updated_at'] = self.updated_at.isoformat()

        dct.pop('_sa_instance_state', None)
        if command == "DEL":
            dct.pop('password', None)

        return dct

    def delete(self):
        """delete the current obj"""
        models.storage.delete(self)
