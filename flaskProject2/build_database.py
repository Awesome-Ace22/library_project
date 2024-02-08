# build_database.py
# creates a small database for testing

from datetime import datetime
from config import flask_app, db
from models import Book, BookDetails
from request import isbn_look_up
BOOKS_NOTES = []

test_data = [9780063237483, 9780872204843, 9781796356304, 9781529091427, 9781627791229]
for isbn in test_data:
    results = isbn_look_up(isbn)
    BOOKS_NOTES.append(results)


with flask_app.app_context():
    db.drop_all()
    db.create_all()
    for data in BOOKS_NOTES:
        new_book = Book(isbn=data.get("isbn"), title=data.get("title"), authors=data.get("authors"))

        # Create BookDetails
        new_book_details = BookDetails(
            publisher=data.get("publisher"),
            publishedDate=data.get("publishedDate"),
            description=data.get("description"),
            thumbnail=data.get("thumbnail")
        )

        new_book.bookdetails = new_book_details
        db.session.add(new_book)
    db.session.commit()
