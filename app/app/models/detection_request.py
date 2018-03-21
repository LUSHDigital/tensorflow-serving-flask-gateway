from marshmallow import Schema, fields, post_load, ValidationError
from PIL import Image
import base64, io

class ImageDetectionRequest(object):
    def __init__(self, model_name=None, image=None, threshold=0.4):
        self.model_name = model_name
        self.image = image
        self.threshold = threshold

    def __repr__(self):
        return '<ImageDetectionRequest(name={self.model_name!r})>'.format(self=self)

class ImageDetectionRequestSchema(Schema):
    @post_load
    def make_user(self, data):
        return ImageDetectionRequest(**data)

    def validate_image(data):
        try:
            im=Image.open(io.BytesIO(base64.b64decode(data)))
        except TypeError as err:
            raise ValidationError('Image TypeError: {0}'.format(err))
        except:
            raise ValidationError('wot??')

    model_name = fields.String(required=True)
    image = fields.Raw(required=True, validate=validate_image)
    threshold = fields.Float()
