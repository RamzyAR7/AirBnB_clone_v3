#!/usr/bin/python3
"""this module for class user"""
import hashlib
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref


class User(BaseModel, Base):
    """class : User to store more data"""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        reviews = relationship("Review",
                               backref=backref("user"),
                               cascade="all, delete-orphan",
                               single_parent=True)
        places = relationship("Place",
                              backref=backref("user"),
                              cascade="all, delete-orphan",
                              single_parent=True)
    else:
        email = ""
        first_name = ""
        last_name = ""
        password = ""

    def __setattr__(self, key, value) -> None:
        '''Sets an attribute of this class to a given value.'''
        if key == 'password':
            hashed_password = hashlib.md5(value.encode())
            super().__setattr__(key, hashed_password.hexdigest())
        else:
            super().__setattr__(key, value)
