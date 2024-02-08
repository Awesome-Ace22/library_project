# models.py

from datetime import datetime
from collections import OrderedDict
from marshmallow import fields

from config import db,ma


class BookDetails(db.Model):
    __tablename__ = "bookdetails"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"),unique=True)
    publisher = db.Column(db.String(255))
    publishedDate = db.Column(db.String(32))
    description = db.Column(db.String)
    thumbnail = db.Column(db.String)

class BookDetailsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookDetails
        load_instance = True
        sqla_session = db.session
        publisher = fields.String()
        publishedDate = fields.String()
        description = fields.String()
        thumbnail = fields.String()

    # Define the order of fields
    ordered_fields = [
        "id", "book_id", "publisher", "publishedDate", "description", "thumbnail"
    ]

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(32), unique=True)
    title = db.Column(db.String(32))
    authors = db.Column(db.String(255))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    bookdetails = db.relationship(
        BookDetails,
        backref="book",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        uselist=False  # Assuming each book has only one set of details
    )


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    id = fields.Int(dump_only=True)
    isbn = fields.String()
    title = fields.String()
    authors = fields.String()
    bookdetails = fields.Nested(BookDetailsSchema)
    timestamp = fields.DateTime(dump_only=True, data_key='timestamp')

    # Define the order of fields
    ordered_fields = [
        'id', 'isbn', 'title', 'authors', 'bookdetails',
        'timestamp'
    ]


book_schema = BookSchema()
books_schema = BookSchema(many=True)
bookdetails_schema = BookDetailsSchema()
