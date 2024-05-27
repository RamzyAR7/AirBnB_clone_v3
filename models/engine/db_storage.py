#!/usr/bin/python3
"""
this module for database storage handling
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User

user = os.getenv("HBNB_MYSQL_USER")
password = os.getenv("HBNB_MYSQL_PWD")
host = os.getenv("HBNB_MYSQL_HOST", default="localhost")
db = os.getenv("HBNB_MYSQL_DB")
env = os.getenv("HBNB_ENV", default="production")
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Class DBStorage for database handling"""
    __engine = None
    __session = None

    def __init__(self):
        """initialaisation of instance"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, password, host,
                                                 db, pool_pre_ping=True))

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a particular class."""
        dct = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        return dct

    def new(self, obj):
        """Adds an object to database"""
        self.__session.add(obj)

    def save(self):
        """Saves changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delets an object from database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload object stored in database"""
        Base.metadata.create_all(self.__engine)
        sesssion_mk = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sesssion_mk)

    def close(self):
        """calls remove or close"""
        self.__session.remove()
