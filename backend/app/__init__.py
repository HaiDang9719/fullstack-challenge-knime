from flask_restplus import Api
from flask import Blueprint
from app.main.namespaces.feature_annotation_namespace import api as feature_annotation_namespace
from app.main.namespaces.correlation_namespace import api as correlation_namespace
from app.main.namespaces.matrix_ordering_namespace import api as matrix_ordering_namespace
from app.main.namespaces.evaluation_namespace import api as evaluation_namespace
from app.main.namespaces.clustering_namespace import api as clustering_namespace
from app.main.namespaces.recommendation_namespace import api as recommendation_namespace
from app.main.namespaces.chatbot_namespace import api as chatbot_namespace

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API for Subspace Annalysis in Automated vArgument Quality Assessment',
          version='2.0',
          description='Retrieving Annotated Features and Subspace Analysis'
          )

api.add_namespace(feature_annotation_namespace, path='/featureAnnotation')
api.add_namespace(correlation_namespace, path='/correlation')
api.add_namespace(matrix_ordering_namespace, path='/matrixOrdering')
api.add_namespace(evaluation_namespace, path='/evaluation')
api.add_namespace(clustering_namespace, path='/clustering')
api.add_namespace(recommendation_namespace, path='/recommendation')
api.add_namespace(chatbot_namespace, path='/chat-bot')