from flask import Flask
from .config import config_by_name


# Application factory pattern to create different instances of the app
def create_app(config_name):
    print("Creating app...")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    return app
