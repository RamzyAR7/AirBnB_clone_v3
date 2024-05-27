# 0x05. AirBnB clone - RESTful API

![AirBnB Logo](https://github.com/RamzyAR7/AirBnB_clone/blob/main/Images/65f4a1dd9c51265f49d0.png)

## Description

This project is part of the Holberton School curriculum and is the continuation of the AirBnB clone project. The focus of this project is to implement MySQL database storage using SQLAlchemy in the existing AirBnB clone project.

## Environment

- Language: Python
- OS: Ubuntu 20.04 LTS
- Style guidelines: [PEP 8 (version 2.8.0)](https://www.python.org/dev/peps/pep-0008/)
- Testing: `unittest` module

## Learning Objectives

- Understand Unit testing and its implementation in a large project
- Learn how to handle *args and **kwargs in Python
- Understand ORM (Object Relational Mapping) and how to use SQLAlchemy
- Learn to create and manage a MySQL database
- Understand the concept of environment variables and how to use them in Python projects

## Files

- All files will be interpreted/compiled on Ubuntu 20.04 LTS using Python3 (version 3.8.5)
- All Python scripts should end with a new line
- All Python scripts must be executable
- The first line of all Python files should be exactly `#!/usr/bin/python3`
- A `README.md` file, at the root of the folder of the project, is mandatory
- All SQL queries should have a comment just before (i.e. syntax above)
- All SQL keywords should be in uppercase (SELECT, WHERE...)
- The length of SQL files will be tested using `wc`
- Each task will have its own folder
- The SQL scripts folder should be named `sql` and placed at the root of the project directory
- The Python unit tests folder should be named `tests` and placed at the root of the project directory


## Comments for your SQL file:
```sql
-- first 3 students in the Batch ID=3
-- because Batch 3 is the best!
SELECT id, name FROM students WHERE batch_id = 3 ORDER BY created_at DESC LIMIT 3;
```

## Tasks

- Ⓜ️ 0. Fork me if you can!------------------COMPLETED ✅
- Ⓜ️ 1. Bug free!----------------------------NOT COMPLETE ❌
- Ⓜ️ 2. Console improvements-----------------COMPLETED ✅
- Ⓜ️ 3. MySQL setup development--------------COMPLETED ✅
- Ⓜ️ 4. MySQL setup test---------------------COMPLETED ✅
- Ⓜ️ 5. Delete object------------------------COMPLETED ✅
- Ⓜ️ 6. DBStorage - States and Cities--------NOT COMPLETE ❌
- Ⓜ️ 7. DBStorage - User---------------------COMPLETED ✅
- Ⓜ️ 8. DBStorage - Placea-------------------NOT COMPLETE ❌
- Ⓜ️ 9. DBStorage - Review-------------------COMPLETED ✅
- Ⓜ️ 10. DBStorage - Amenity... and BOOM!-----NOT COMPLETE ❌

## Developers:

| **Ahmed Ramzy (AKA Ramzy)** | **Mahmoud Metwalli (AKA Metwalli)** |
|---|---|
|[@Ahmed Ramzy](https://www.github.com/RamzyAR7) | [@Mahmoud Metwalli](https://github.com/MahmoudMetwalli)|
| ![Ahmed Ramzy](https://github.com/RamzyAR7/AirBnB_clone/blob/main/Images/image%20(1).png) | ![Mahmoud Metwalli](https://github.com/RamzyAR7/AirBnB_clone/blob/main/Images/image%20(2).png)|
