from config import flask_app, db
from models import User, user_schema, users_schema, Library, library_schema, Book,book_schema, books_schema
from request import isbn_look_up
from set_up_database import reset_database
from create_database import create_db

ctx = flask_app.app_context()
ctx.push()

#9781529091427

users = users_schema.dump(User.query.all())
books = books_schema.dump(Book.query.all())
USER_DATA = []
for user_data in users:
    libraries = []
    for item in user_data["libraries"]:
        library = {
            "library_name": user_data["libraries"][0]["library_name"],
            "library_books": user_data["libraries"][0]["books"]
        }
        libraries.append(library)
    user = {
        "username": user_data["username"],
        "password": user_data["password"],
        "libraries": libraries
    }
    USER_DATA.append(user)

"""
    USER_DATA = [
    {
        "username": "test_username",
        "password": "test_password",
        "libraries": [{
            "library_name": "test_library",
            "library_books": books
        }]
    },
    ]
"""

def insert_user(username,password):
    user = {
        "username": username,
        "password": password,
        "libraries": []
    }
    # user_schema.load(user, session=db.session)
    # db.session.commit()
    USER_DATA.append(user)
    reset_db()

def insert_library(username,library_name):
    user = User.query.filter_by(username=username).first()
    library = {
        "library_name": library_name or f"{username}'s Library",
        "library_books": []
    }
    if user:
        USER_DATA[user.user_id - 1]["libraries"].append(library)
    reset_db()

def insert_book(isbn,username):
    results = isbn_look_up(isbn)
    user = User.query.filter_by(username=username).first()
    if user:
        USER_DATA[user.user_id - 1]["libraries"][0]["library_books"].append(results)
    reset_db()


def reset_db():
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        for user in USER_DATA:
            new_user = User(username=user.get("username"), password=user.get("password"))
            for library in user.get("libraries", []):
                new_library = Library(library_name=user["libraries"][0]["library_name"])
                for book in user["libraries"][0]["library_books"]:
                    new_book = Book(
                        # book_id=book.get("id"),
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


def read_all_users():

    users = User.query.all()
    return users_schema.dump(users)

if __name__ == '__main__':
    insert_user("amelia", "12345")
    insert_library("amelia", "amelia's Library")
    reset_db()

