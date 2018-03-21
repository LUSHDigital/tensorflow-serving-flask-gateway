from marshmallow import Schema, fields, post_load, ValidationError
from PIL import Image
import base64, io
from detection import DetectionSchema

class DetectionResponse(object):
    def __init__(self, detections=[], tfserve_time=None, controller_time=None):
        self.detections = detections
        self.tfserve_time = tfserve_time
        self.controller_time = controller_time

class DetectionResponseSchema(Schema):
    tfserve_time = fields.Float()
    detections = fields.Nested(DetectionSchema, many=True)
    controller_time = fields.Float()
