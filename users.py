# users.py
import os
from flask import abort, make_response
from config import db
from models import User, user_schema, users_schema, Library, Book, books_schema, book_schema
from request import isbn_look_up

def check_login(attempted_username, attempted_password):
    if attempted_username == 'admin' and attempted_password == '12345':
        return True
    else:
        user = user_schema.dump(User.query.filter_by(username=attempted_username).first())
        if user is None:
            return False
        elif attempted_password == user.get('password'):
            return True

def read_all_users():
    users = User.query.all()
    return users_schema.dump(users)


def read_user(username):
    user = user_schema.dump(User.query.filter_by(username=username).first())
    return user_schema.dump(user)


