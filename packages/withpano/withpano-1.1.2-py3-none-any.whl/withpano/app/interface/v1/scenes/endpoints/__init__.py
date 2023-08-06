import logging
import os
from http.client import responses

from flask import request
from flask_restx import Resource
from werkzeug.utils import secure_filename

from withpano.app.interface import api
from withpano.app.interface.v1.scenes.parser import upload_parser
from withpano.app.interface.v1.scenes.type import FileValidation
from withpano.app.libraries.hotspot import Hotspot
from withpano.app.libraries.scenes import Scenes
from main import server

log = logging.getLogger('console')

ns = api.namespace('scenes', description='Add/Update/Comment')


@ns.route('/create/')
class SceneCreate(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        print(args)
        uploaded_file = args['file']  # This is FileStorage instance
        validate = FileValidation.allowed_file(uploaded_file)
        scene = Scenes()
        if not scene.check_scene_exist(args['name']):
            if validate:
                filename = secure_filename(uploaded_file.filename)
                extension = filename.split('.')[-1]
                new_filename = "upload-{}.{}".format(
                    args['name'], extension
                )
                uploaded_file.save(os.path.join(f"{server.config['STATIC_PATH']}/scene_uploaded_img", new_filename))
                scene.create_scene(args['name'], new_filename)
                return {'url': uploaded_file.filename}, 201
            return {"message": "File Format not supported"}, 500
        return {"message": "Scene Already exist, Try Different Name"}, 500


@ns.route('/scene/<string:scene>')
class SceneRequest(Resource):
    @ns.doc(responses=responses)
    def get(self, scene):
        scenes = Scenes()
        return scenes.get_scene(scene)


@ns.route('/scene/save/<string:scene>')
class SceneSaveDataRequest(Resource):
    @ns.doc(responses=responses)
    def post(self, scene):
        scenes = Scenes()
        return scenes.save_scene(scene, request.json)


# HOTSPOT

@ns.route('/hotspot/<string:scene>')
class SceneHotsPotRequest(Resource):
    @ns.doc(responses=responses)
    def get(self, scene):
        hotspot = Hotspot()
        return hotspot.get_all_hotspot(scene)


@ns.route('/scene/hotspot/<string:scene>/<string:hid>')
class SceneHotsPotRequest(Resource):
    @ns.doc(responses=responses)
    def get(self, scene, hid):
        hotspot = Hotspot()
        return hotspot.get_hotspot(scene,hid)


# @crossdomain(origin='*', headers=['Access-Control-Allow-Origin', '*'])
@ns.route('/scene/hotspot/<string:scene>')
class SceneHotsPotCreateRequest(Resource):
    @ns.doc(responses=responses)
    # @ns.expect(create_model)
    def post(self, scene):
        print(scene)
        print(request.json)
        # hotspot = Hotspot()
        # return hotspot.create_hotspot(scene, request.json)
        return None
