#!/usr/bin/python3
"""this module for class city"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class City(BaseModel, Base):
    """class : City to store more data"""
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"),
                          nullable=False)
        places = relationship("Place",
                              backref=backref("cities"),
                              cascade="all, delete-orphan",
                              single_parent=True)
    else:
        name = ""
        state_id = ""
