from main import app,read_book
from books import read_one

#pushes app context to use functionality that needs the full application
ctx = app.app_context()
ctx.push()


print(read_one(9780872204843))
