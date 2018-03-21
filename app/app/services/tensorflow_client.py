from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from google.protobuf.json_format import MessageToDict
from PIL import Image

import tensorflow as tf
import numpy as np
import time
import base64, io, json

from app.models.detection_response import DetectionResponse, DetectionResponseSchema
from app.models.detection import Detection, DetectionSchema
from app.models.hit_box import HitBox, HitBoxSchema
from pprint import pprint

class TensorflowServeClient:

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

    def inference(self, model_name, image_base64, threshold, tfs_host, tfs_port):
        channel = implementations.insecure_channel(tfs_host, tfs_port)
        stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
        # Send request
        # Create prediction request object
        request = predict_pb2.PredictRequest()

        # Specify model name (must be the same as when the TensorFlow serving serving was started)
        request.model_spec.name = model_name

        # Initalize prediction
        # Specify signature name (should be the same as specified when exporting model)
        request.model_spec.signature_name = "detection_signature"

        # Read image from b64 encoded string
        image = Image.open(io.BytesIO(base64.b64decode(image_base64)))

        # Take image an load into a Numpy array
        image_np = self.load_image_into_numpy_array(image)

        # Expand dimensions.  Not really sure what this does
        image_np_expanded = np.expand_dims(image_np, axis=0)

        # Build request
        request.inputs['inputs'].CopyFrom(
            tf.contrib.util.make_tensor_proto(image_np_expanded,
                shape=image_np_expanded.shape, dtype='uint8'))

        # Start timer so we can time the TensorServe request and response
        start_time = time.time()

        # Run prediction against TensorServe
        result = stub.Predict(request, 10.0)  # 10 secs timeout

        # Record end time, so we can calculate difference
        end_time = time.time()

        # Calculate time take and formate nicely
        time_taken = "{:.2f}".format(end_time - start_time)

        detectionScores = result.outputs['detection_scores'].float_val
        detectionClasses = result.outputs['detection_classes'].float_val
        detectionBoxes = result.outputs['detection_boxes'].float_val

        detectionBoxes = map(None, *([iter(detectionBoxes)] * 4))

        detectionResponse = DetectionResponse()
        detectionResponse.tfserve_time = time_taken
        detections = []

        for idx, score in enumerate(detectionScores):
            if score > threshold:
                detectionResult = Detection()
                detectionResult.score = score
                detectionResult.class_id = detectionClasses[idx]
                detectionResult.hit_box = HitBox(detectionBoxes[idx][0],detectionBoxes[idx][1],detectionBoxes[idx][2],detectionBoxes[idx][3])
                detections.append(detectionResult)
            else:
                break

        detectionResponse.detections = detections

        return detectionResponse
