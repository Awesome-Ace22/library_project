# Version 1.0
# i installed brew,node, etc for https://reactnative.dev/docs/environment-setup?package-manager=npm
# Warning: The post-install step did not complete successfully
# You can try again using:
# brew postinstall node
# exurbia adress https://m.media-amazon.com/images/I/61OPJ7+h5bL._AC_UF1000,1000_QL80_.jpg
# Access denied: chrome://net-internals/#sockets --> Flush Socket Pools

from flask import render_template,session, redirect, url_for, request, send_file
from request import isbn_look_up
from config import connex_app, db
from models import Book, books_schema, book_schema
from insert_in_database import insert_book
from books import read_all, read_one, create
from images import fetch_image
from users import check_login, create_user, read_all_users, read_user
import logging
import functools

from io import BytesIO

# Add the API definition
connex_app.add_api("swagger.yml")

# Get the Flask app instance from connex_app
app = connex_app.app

logging.basicConfig(level=logging.DEBUG)

# Details on the Secret Key: https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing the session data.
app.secret_key = 'BAD_SECRET_KEY'



def get_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

def login_required(func):
    """Make sure user is logged in before proceeding"""
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if session['username'] is None:
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return wrapper_login_required


# Define the route
@app.route("/", methods=['GET','POST'])
def home():
    app.logger.info('Processing default request')
    books = Book.query.all()
    return render_template("home.html")


@app.route("/userlogin/", methods=['GET', 'POST'])
def user_login():
    error = ''
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        login_attempt = check_login(attempted_username,attempted_password)
        if login_attempt:
            session['username'] = attempted_username
            return redirect(url_for('user_library', username=attempted_username))
        else:
            print('invalid credentials')
            error = 'Invalid credentials. Please, try again.'
    return render_template('home.html', error=error)

@app.route("/logout", methods=['GET', 'POST'])
def user_logout():
    session.pop('username', default=None)
    return render_template('home.html')


@app.route("/signupuser/", methods=['GET', 'POST'])
def sign_up_user():
    error = ''
    if request.method == "POST":
        new_username = request.form['username']
        new_password = request.form['password']
        sign_up_attempt = create_user(new_username,new_password)
        if sign_up_attempt:
            error = "success"
            session['username'] = new_username
            return render_template('user_library', username=new_username)
            # return redirect(url_for('user_library', username=new_username))
        else:
            print('Invalid Username')
            error = f"User with Username: {new_username} already exists. Please, try again"
    return render_template('home.html', error=error)
@app.route("/allusers", methods=['GET', 'POST'])
def all_users():
    users = read_all_users()
    return users


@app.route("/userlibrary/<username>", methods=['GET', 'POST'])
@login_required
def user_library(username):
    error = ''
    if request.method == "POST":
        username = request.form['username']
    if username == session['username']:
        user = read_user(username)
        session['library_id'] = user["libraries"][0]["library_id"]
        books = user["libraries"][0]["books"]
        list = [1,2,3,4,5,6,7,8,9,10]
        return render_template("library.html", books=books)
    else: render_template('home.html',error=error)

@app.route("/read_books", methods=['GET'])
def read_books():
    username = "test_username"
    user = read_user(username)
    books = user["libraries"][0]["books"]
    return books


@app.route("/read_book/<isbn>", methods=['GET','POST'])
@login_required
def read_book(isbn):
    if request.method == "POST":
        isbn = request.form['isbn']
    library_id = session['library_id']
    book = read_one(isbn,library_id)
    return render_template("book_info.html", book=book)

@app.route('/add_new/<isbn>', methods=['GET', 'POST'])
def add_new(isbn):
    if request.method == "POST":
        isbn = request.form['isbn']
        username = session['username']
        insert_book(isbn,username)
        return redirect(url_for('read_book', isbn=isbn))

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






