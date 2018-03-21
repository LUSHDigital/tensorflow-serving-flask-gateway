from flask_restful import Resource
from flask import jsonify, request, current_app
from app.models.detection_request import ImageDetectionRequest, ImageDetectionRequestSchema
from app.models.detection_response import DetectionResponse, DetectionResponseSchema

import pprint
import time
from app.services.tensorflow_client import *

class ImageDetection(Resource):

    def __init__(self, tfs_host, tfs_port):
        self.tfs_host = tfs_host
        self.tfs_port = tfs_port

    def post(self):
        start_time = time.time()
        imageDetectionRequestSchema = ImageDetectionRequestSchema()
        tensorflowServeClient = TensorflowServeClient()

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = imageDetectionRequestSchema.load(json_data)
        if errors:
            return errors, 422

        result = tensorflowServeClient.inference(data.model_name, data.image, data.threshold, self.tfs_host, self.tfs_port)

        if type(result) is DetectionResponse:
            end_time = time.time()
            result.controller_time = "{:.2f}".format(time.time() - start_time)
            return DetectionResponseSchema().dump(result)
        else:
            return {'message': 'Something bad happened'}, 400
