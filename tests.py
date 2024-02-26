from main import app,read_book
from books import read_one
from models import User,user_schema,Library, Book, books_schema, book_schema
from users import read_all_users
#pushes app context to use functionality that needs the full application
ctx = app.app_context()
ctx.push()



attempted_username = "test_username"
user = user_schema.dump(User.query.filter_by(username=attempted_username).first())
library = user["libraries"][0]
books = user["libraries"][0]["books"][0]
print(user)
print(library)
print(books)

users = read_all_users()

