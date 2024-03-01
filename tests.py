from main import app,read_book
from books import read_one
from models import User,user_schema,Library, Book, books_schema, book_schema
from users import read_all_users,create_user, delete_user
from insert_in_database import insert_user,insert_library, insert_book
#pushes app context to use functionality that needs the full application
ctx = app.app_context()
ctx.push()

if __name__ == "__main__":
    username = "test_username"
    password = "12345"
    isbn = "9781338635171"
    library_id = "1"
    insert_book(isbn, username)
    read_one(isbn,library_id)
    #print(create_user(username,password))
    #print(library)
    #print(books)



"""
attempted_username = "test_username"
user = user_schema.dump(User.query.filter_by(username=attempted_username).first())
library = user["libraries"][0]
books = user["libraries"][0]["books"][0]
print(user)
print(library)
print(books)

users = read_all_users()
"""



