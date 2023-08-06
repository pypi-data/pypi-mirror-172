from flask_restx import fields

from withpano.app.interface import api

get_parser = api.parser()
get_parser.add_argument('account_id', type=str, required=False)
POSITION_MODEL = api.model("position", dict(
    x=fields.Integer(),
    y=fields.Integer(),
    yaw=fields.Float(),
    pitch=fields.Float(),
))
TRANSFORM_MODEL = api.model(
    "transform",
    {
        "x": fields.Integer(),
        "y": fields.Integer(),
        "yaw": fields.Float(),
        "pitch": fields.Float(),
    }
)
create_model = api.model(
    'Create HotsPot',
    {
        'elementId': fields.String(required=True),
        'name': fields.String(required=True),
        'type': fields.String(),
        'position': fields.Nested(POSITION_MODEL),
        'radius': fields.String(),
        'transform': fields.String(),
        'className': fields.String()
    }
)
