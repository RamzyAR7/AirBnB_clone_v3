#!/usr/bin/python3
""" for reload data every process"""
import os


storage_t = os.getenv("HBNB_TYPE_STORAGE")


if os.getenv('HBNB_TYPE_STORAGE') == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
