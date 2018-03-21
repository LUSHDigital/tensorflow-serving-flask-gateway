# TensorFlow Serving Flask Gateway

A Python Flask based proxy service to allow clients to run simple object detection inference against a TensorFlow Serving instance, without using gRPC.

## Deployment

Assuming you have a functioning TensorFlow Serving instance that has an object detection model running, edit the included [Dockerfile](Dockerfile) and set the following environment variables:

    ENV APP_TFSERVING_HOST 0.0.0.0
    ENV APP_TFSERVING_PORT 8080

Where `APP_TFSERVING_HOST` is the host address of your TensorFlow Serving instance, and `APP_TFSERVING_PORT` is the port that it is listening on.

Next, build the Docker image using:

    docker build -t flask_tf_serve .

This image can then be run:

    docker run --rm -ti -p 8080:80 flask_tf_serve

## Usage

To use the gateway, POST a request to:

    http://0.0.0.0:8080/imageDetection

With the following JSON body, where `--IMAGE--` is a `Base64` encoded version of a jpeg that you wish to run object detection on.

```json
{
    "model_name": "model_name",
    "threshold" : 0.04,
    "image" : "--IMAGE--"
}
```

The returned JSON will look something like this:

```json
{
    "detections": [
        {
            "class_id": 44,
            "score": 0.4619715213775635,
            "class_label": null,
            "hit_box": {
                "y1": 0.11837565898895264,
                "x2": 0.9808037281036377,
                "x1": 0.2933504283428192,
                "y2": 0.8071466684341431
            }
        },
        {
            "class_id": 74,
            "score": 0.07420706003904343,
            "class_label": null,
            "hit_box": {
                "y1": 0.10970744490623474,
                "x2": 0.9801961183547974,
                "x1": 0.33997276425361633,
                "y2": 0.7276654243469238
            }
        }
    ],
    "controller_time": 0.39,
    "tfserve_time": 0.31
}
```


## Built With

* [Flask](http://flask.pocoo.org/) - A Python Microframework
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - A Flask that adds support for quickly building REST APIs
* [TensorFlow](https://www.tensorflow.org/) - An open-source machine learning framework for everyone.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/LUSHDigital/tensorflow-serving-flask-gateway/tags).

## Authors

* **Chris Hemmings** - *Initial work* - [chrishemmings](https://github.com/chrishemmings)
* **Dan Potepa** - *Initial work* - [cuotos](https://github.com/cuotos)

See also the list of [contributors](https://github.com/LUSHDigital/tensorflow-serving-flask-gateway/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
