from config import flask_app, db
from models import User, user_schema, users_schema, Library, library_schema, Book,book_schema, books_schema
from request import isbn_look_up
#9781529091427

books = books_schema.dump(Book.query.all())
USER_DATA = [
    {
        "username": "test_username",
        "password": "test_password",
        "libraries": [{
            "library_name": "test_library",
            "library_books": books
        }]
    }
    ]

def insert_user(username,password):
    user = {
        "username": username,
        "password": password,
        "libraries": []
    }
    USER_DATA.append(user)
    #reset_db()

def insert_library(username,library_name):
    user = User.query.filter_by(username=username).first()
    library = {
        "library_name": library_name or f"{username}'s Library",
        "library_books": []
    }
    if user:
        USER_DATA[user.user_id - 1]["libraries"].append(library)
        #reset_db()


def insert_book(isbn):
    results = isbn_look_up(isbn)
    books.append(results)
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





