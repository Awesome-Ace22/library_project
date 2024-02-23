from flask import Flask
from config import connex_app
from library import pages
def create_app():
    app = connex_app.app
    app.register_blueprint(pages.bp)
    return app