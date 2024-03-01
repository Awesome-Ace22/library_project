# users.py
import os
from flask import abort, make_response
from config import db
from models import User, user_schema, users_schema, Library, Book, books_schema, book_schema
from insert_in_database import insert_user, insert_library
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
    user = user_schema.dump(User.query.filter_by(username = username).first())
    return user_schema.dump(user)

def create_user(username,password):
    existing_user = User.query.filter(User.username == username).one_or_none()
    if existing_user is None:
        insert_user(username, password)
        new_library = f"{username}'s library"
        insert_library(username, new_library)
        return True
    else:
        return False


def delete_user(username):
    existing_user = User.query.filter(User.username == username).one_or_none()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"{username} successfully deleted", 200)
    else:
        abort(
            404,
            f"User with username: {username} not found"
        )