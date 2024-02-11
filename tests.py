from main import app,read_book
from books import read_one
from models import User,user_schema,Library, Book, books_schema, book_schema

#pushes app context to use functionality that needs the full application
ctx = app.app_context()
ctx.push()


print(read_one(9780872204843))
attempted_username = "test_username"
user = user_schema.dump(User.query.filter_by(username=attempted_username).first())
print(user)
print(user.get('password'))
