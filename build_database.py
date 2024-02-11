
import urllib.request
import urllib.parse
import json
from flask import jsonify
from config import flask_app, db
from models import User, Library, Book
from request import isbn_look_up
from set_up_database import reset_database
from create_database import create_db


BOOKS_NOTES = []

test_data = [9780063237483, 9780872204843, 9781796356304, 9781529091427, 9781627791229]
for isbn in test_data:
    results = isbn_look_up(isbn)
    BOOKS_NOTES.append(results)

for bk in BOOKS_NOTES:
    for key in bk:
        format_string = '"' + key + '"' + ": {" + key + "}"
        # print(format_string.format(**bk))

USER_DATA = [
    {
        "username": "test_username",
        "password": "test_password",
        "libraries": [{
            "library_name": "test_library",
            "library_books": BOOKS_NOTES
        }]
    }
]




def fill_database():
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        for user in USER_DATA:
            new_user = User(username=user.get("username"), password=user.get("password"))
            for library in user.get("libraries",[]):
                new_library = Library(library_name=user["libraries"][0]["library_name"])
                for book in user["libraries"][0]["library_books"]:
                    new_book = Book(
                        #book_id=book.get("id"),
                        isbn=book.get("isbn"),
                        title=book.get("title"),
                        authors=book.get("authors"),
                        publisher=book.get("publisher"),
                        publishedDate=book.get("publishedDate"),
                        description=book.get("description"),
                        pageCount=book.get("pageCount"),
                        thumbnail=book.get("thumbnail")
                    )
                    new_library.books.append(new_book)
                new_user.libraries.append(new_library)
            db.session.add(new_user)
        db.session.commit()


if __name__ == '__main__':
    reset_database()
    create_db()
    fill_database()



# print(BOOKS_NOTES)
"""
users = [
    {
        "username": "test_username",
        "password": "test_password",
        "libraries": [{
            "library_name": "test_library",
            "library_books": [
                {
                    "isbn": 9780872204843,
                    "title": "Odyssey",
                    "authors":"Homer",
                    "description": "Lombardo's Odyssey offers the distinctive speed, clarity, and boldness that so distinguished his 1997 Iliad .",
                    "pageCount": 504,
                    "thumbnail": "http://books.google.com/books/content?id=2vZhQgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
                    "publisher": "Hackett Publishing Company Incorporated",
                    "publishedDate":"2000",},
                {
                    "isbn": 9781627791229,
                    "title": "The Book of Three, 50th Anniversary Edition",
                    "authors": "Lloyd Alexander",
                    "description": "Taran, Assistant Pig-Keeper to a famous oracular sow, sets out on a hazardous mission to save Prydain from the forces of evil.",
                    "pageCount": 204,
                    "thumbnail": "http://books.google.com/books/content?id=qXYtBAAAQBAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
                    "publisher": "Macmillan",
                    "publishedDate":"2014-09-23",}
            ]
        }],
    }
]
"""