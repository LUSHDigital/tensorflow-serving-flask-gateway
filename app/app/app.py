from flask import Flask
from flask_restful import Api
from controllers import *
from services.tensorflow_client import *
import os
# from dotenv import load_dotenv
#
# load_dotenv(verbose=True)

tfs_host = os.getenv("APP_TFSERVING_HOST")
tfs_port = int(os.getenv("APP_TFSERVING_PORT"))

app = Flask(__name__)
api = Api(app)

api.add_resource(ImageDetection, '/imageDetection', '/imageDetection/<string:id>', resource_class_kwargs={'tfs_host': tfs_host, 'tfs_port' : tfs_port})

if __name__ == '__main__':
    app.run(debug=True)
