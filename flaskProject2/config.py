# config.py

import pathlib
#import connexion
from connexion import FlaskApp
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
#connex_app = connexion.App(__name__, specification_dir=basedir)
connex_app = FlaskApp(__name__, specification_dir=basedir)



# Create a Flask app instance
flask_app = connex_app.app
flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'books.db'}"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(flask_app)
ma = Marshmallow(flask_app)