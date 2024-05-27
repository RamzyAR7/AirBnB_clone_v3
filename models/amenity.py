#!/usr/bin/python3
"""this module for class amenity"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """class : Amenity to store more data about amenities"""
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""
