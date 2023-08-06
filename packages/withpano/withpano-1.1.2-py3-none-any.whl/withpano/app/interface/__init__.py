# Create an APISpec
from flask_restx import Api

from main import server

api = Api(server, title='withpano_API', doc='/doc', prefix='/withpano')
