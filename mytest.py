#!/usr/bin/python3
"""Hi there"""
from models.user import User


if __name__ == '__main__':
    user = User()
    user.password = "H2223"
    print(user.password)
