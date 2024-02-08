# book.py

from flask import abort, make_response
from config import db
from models import Book, books_schema, book_schema, bookdetails_schema

def read_all():
    results = books_schema.dump(Book.query.all())
    books = []  # [book[field] for field in ordered_fields]
    for book in results:
        orderedbook = []
        for field, data in book.items():
            orderedbook.append((field, data))
        books.append(orderedbook)
    return books


def read_one(isbn):
    result = Book.query.filter(Book.isbn == isbn).one_or_none()

    if result is not None:
        book = book_schema.dump(result)
        return book
    else:
        abort(
            404, f"Book with ISBN: {isbn} not found"
        )

def sort_info(dict):
    desired_order = ['id', 'isbn', 'title', 'authors', ["id", "book_id", "publisher", "publishedDate", "description", "thumbnail"], 'timestamp']
    def custom_order(key):
        for i, order in enumerate(desired_order):
            if isinstance(order, list) and key in order:
                return i
            elif key == order:
                return i
        return len(desired_order)

    sorted_dict = dict(sorted(dict.items(), key=lambda item: custom_order(item[0])))
    return sorted_dict


def create(book_data):
    isbn = book_data.get("isbn")
    existing_book = Book.query.filter(Book.isbn == isbn).one_or_none()

    if existing_book is None:
        # Create a new Book instance
        new_book = book_schema.load(book_data, session=db.session)
        db.session.add(new_book)
        db.session.commit()

        # Create associated BookDetails
        book_details_data = {
            "id": new_book.id,
            "publisher": book_data.get("publisher"),
            "publishedDate": book_data.get("publishedDate"),
            "description": book_data.get("description"),
            "thumbnail": book_data.get("thumbnail")
        }

        new_book_details = bookdetails_schema.load(book_details_data, session=db.session)
        db.session.add(new_book_details)
        db.session.commit()

        return book_schema.dump(new_book), 201
    else:
        abort(
            406,
            f"Book with ISBN: {isbn} already exists",
        )



def update(isbn, book):
    existing_book = Book.query.filter(Book.isbn == isbn).one_or_none()

    if existing_book:
        update_book = book_schema.load(book, session=db.session)
        existing_book.title = update_book.title
        existing_book.title = update_book.title
        existing_book.authors = update_book.authors
        existing_book.publisher = update_book.publisher
        existing_book.publishedDate = update_book.publishedDate
        existing_book.description = update_book.description
        existing_book.thumbnail = update_book.thumbnail

        db.session.merge(existing_book)
        db.session.commit()
        return book_schema.dump(existing_book), 201
    else:
        abort(
            404,
            f"Book with ISBN: {isbn} not found"
        )


def delete(isbn):
    existing_book = Book.query.filter(Book.isbn == isbn).one_or_none()
    if existing_book:
        db.session.delete(existing_book)
        db.session.commit()
        return make_response(f"{isbn} successfully deleted", 200)
    else:
        abort(
            404,
            f"Book with ISBN: {isbn} not found"
        )