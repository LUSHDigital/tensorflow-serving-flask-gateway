from marshmallow import Schema, fields, post_load, ValidationError
from PIL import Image
import base64, io

class HitBox(object):
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class HitBoxSchema(Schema):
    x1 = fields.Float()
    y1 = fields.Float()
    x2 = fields.Float()
    y2 = fields.Float()
