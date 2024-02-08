# bookdetails.py

from config import db
from models import BookDetails, bookdetails_schema

def create(book_details_data):
    new_book_details = BookDetails(**book_details_data)
    db.session.add(new_book_details)
    db.session.commit()
    return bookdetails_schema.dump(new_book_details), 201


def read_all():
    details = BookDetails.query.all()
    return bookdetails_schema.dump(details)