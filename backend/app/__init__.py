from flask_restplus import Api
from flask import Blueprint
from app.main.namespaces.search_namespace import api as search_namespace

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API for Fullstack Challenge KNIME',
          version='1.0',
          description='Search APIs'
          )

api.add_namespace(search_namespace, path='/search')