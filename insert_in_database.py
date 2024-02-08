from config import flask_app, db
from models import Book, BookDetails, books_schema,bookdetails_schema
from request import isbn_look_up
#9781529091427

def insert_in_database(isbn):
    books = books_schema.dump(Book.query.all())
    results = isbn_look_up(isbn)
    books.append(results)

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        for data in books:
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
