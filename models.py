# models.py


'''
Class Structure:
user > library > books

add later:
 - library > collections > books
 - books > imageData
'''
from datetime import datetime

from marshmallow import fields
from config import db, ma

noImage="https://png.pngtree.com/png-vector/20190820/ourmid/pngtree-no-image-vector-illustration-isolated-png-image_1694547.jpg"

class Book(db.Model):
    __tablename__ = "book"
    __table_args__ = {'keep_existing': True}
    book_id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey("library.library_id"))
    isbn = db.Column(db.String(32)) #unique=True
    title = db.Column(db.String(32))
    authors = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    publishedDate = db.Column(db.String(32))
    description = db.Column(db.String)
    pageCount = db.Column(db.Integer)
    thumbnail = db.Column(db.String,default=noImage)

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
        sqla_session = db.session
        book_id = fields.Int(dump_only=True)
        isbn = fields.String()
        title = fields.String()
        authors = fields.String()
        publisher = fields.String()
        publishedDate = fields.String()
        description = fields.String()
        pageCount = fields.Int()
        thumbnail = fields.String()
        include_fk = True


class Library(db.Model):
    __tablename__ = "library"
    __table_args__ = {'keep_existing': True}
    library_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    library_name = db.Column(db.String(32))
    books = db.relationship(
        Book,
        backref="library",
        cascade="all, delete, delete-orphan",
        single_parent=True,
    )


class LibrarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Library
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True

    user_id = fields.Int(dump_only=True)
    library_name = fields.String()
    books = fields.Nested(BookSchema(many=True))


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'keep_existing': True}
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    libraries = db.relationship(
        Library,
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        #uselist=False  # each user only has one library
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    libraries = fields.Nested(LibrarySchema(many=True))

book_schema = BookSchema()
books_schema = BookSchema(many=True)
library_schema = LibrarySchema()
libraries_schema = LibrarySchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
