#!/usr/bin/python3
"""this module for class place"""
from models.base_model import BaseModel, Base
import models
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship, backref
from models.amenity import Amenity

if getenv('HBNB_TYPE_STORAGE') == "db":
    place_amenity = Table('association', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False)
                          )


class Place(BaseModel, Base):
    """class : Place to store more data"""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review",
                               backref=backref("place"),
                               cascade="all, delete-orphan",
                               single_parent=True)
        place_amenities = relationship("Amenity",
                                       secondary=place_amenity,
                                       backref="place_amenities",
                                       viewonly=False)
        amenity_ids = []
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter attribute to retrieve associated with this place."""
            reviews = models.storage.all("Review")
            return [review for review in reviews.values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """ Get Linked Amenities"""
            amenitylist = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenitylist.append(amenity)
            return amenitylist

        @amenities.setter
        def amenities(self, obj):
            """To add amenities"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
