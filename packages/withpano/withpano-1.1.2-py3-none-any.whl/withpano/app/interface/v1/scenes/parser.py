from werkzeug.datastructures import FileStorage

from withpano.app.interface import api

upload_parser = api.parser()
upload_parser.add_argument('name', location='form', required=True, help="Name cannot be blank!")
upload_parser.add_argument('face_size', location='form', required=True, help="FaceSize cannot be blank!")
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
