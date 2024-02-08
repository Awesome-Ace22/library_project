# Version 1.0

from flask import render_template, redirect, url_for, request, send_file
from request import isbn_look_up
from config import connex_app, db
from models import Book, books_schema, book_schema
from insert_in_database import insert_in_database
from books import read_all, read_one
from images import fetch_image
import logging
from io import BytesIO

# Add the API definition
connex_app.add_api("swagger.yml")

# Get the Flask app instance from connex_app
app = connex_app.app

logging.basicConfig(level=logging.DEBUG)


def get_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'



# Define the route
@app.route("/", methods=['GET','POST'])
def home():
    app.logger.info('Processing default request')
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/read_books", methods=['GET'])
def read_books():
    books = read_all()
    return books


@app.route("/read_book/<isbn>", methods=['GET','POST'])
def read_book(isbn):
    if request.method == "POST":
        isbn = request.form['isbn']

    book_data = book_schema.dump(Book.query.filter(Book.isbn == isbn).one_or_none())
    #book = (f'{book_data}') #sort_info(book_data)
    return render_template("book.html", book=book_data)

@app.route('/add_new/<isbn>', methods=['GET', 'POST'])
def add_new(isbn):
    if request.method == "POST":
        isbn = request.form['isbn']
        insert_in_database(isbn)
        return redirect(url_for('/read_book/<isbn>', isbn=isbn))

    else:
        # results = isbn_look_up(isbn)
        # json_data = json.dumps(results, indent=4, sort_keys=True)
        insert_in_database(isbn)
        return redirect(url_for('/read_book/<isbn>', isbn=isbn))

@app.route('/image<isbn>.png')
def thumbnail(isbn):
    image_data = fetch_image(isbn)
    if image_data:
        response = send_file(image_data, mimetype='image/jpeg')
        get_headers(response)
        return response

    else:
        return "Failed to serve image."
    #get_headers(response)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)




