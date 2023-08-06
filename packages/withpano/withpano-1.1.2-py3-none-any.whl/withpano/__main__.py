from flask import send_from_directory, Blueprint
from flask_cors import CORS  # comment this on deployment

from withpano.app.interface import api
from withpano.config import BaseConfig
from main import server

# App Config Initiate from ENV Object
server.config.from_object(BaseConfig)
server.static_folder = server.config['STATIC_PATH']


# CORS Enabled
# server.config["CORS_HEADERS"] = "Content-Type"
CORS(server)


@server.route("/", defaults={'path': ''})
@server.route("/<string:path>")
def serve_main(path):
    return send_from_directory(server.static_folder, 'index.html')


@server.route("/manifest.json")
def manifest():
    return send_from_directory(server.static_folder, 'manifest.json')


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(server.static_folder, 'favicon.ico')


# Import Namespace
from withpano.app.interface.v1.scenes.endpoints import ns as file_ns

# API Interface register
blueprint_api = Blueprint(
    'api', __name__,
    url_prefix='{}api/v1'.format(server.config['APP_URL_PREFIX']),
    # static_url_path='/static/site',
    static_folder='static'
)
# CORS(blueprint_api, resources='*', allow_headers='*', origins='*', expose_headers='Authorization')

# @blueprint_api.after_request
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = '*'
#     # Other headers can be added here if needed
#     return response


api.init_app(blueprint_api)
api.add_namespace(file_ns)
server.register_blueprint(blueprint_api)

# with server.app_context():
#     print(url_for('site.static', filename='upload-TestNew.jpg'))

if __name__ == '__main__':
    server.run(debug=True, threaded=True, host='0.0.0.0', port=8090, use_reloader=True)
    # serve(server, host="0.0.0.0", port=8090, ident="meta", threads=4, cleanup_interval=10)
