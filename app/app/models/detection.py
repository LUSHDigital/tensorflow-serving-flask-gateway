from marshmallow import Schema, fields, post_load, ValidationError
from PIL import Image
import base64, io
from hit_box import HitBoxSchema

class Detection(object):
    def __init__(self, score=None, class_id=None, class_label=None, hit_box=None):
        self.score = score
        self.class_id = class_id
        self.class_label = class_label
        self.hit_box = hit_box

class DetectionSchema(Schema):
    score = fields.Float()
    class_id = fields.Int()
    class_label = fields.String()
    hit_box = fields.Nested(HitBoxSchema)
