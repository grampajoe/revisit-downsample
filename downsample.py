import base64
import random
from flask import Flask, jsonify, request
from PIL import Image
from StringIO import StringIO


app = Flask('downsample')


@app.route('/')
def index():
    """Returns a 200, that's about it!!!!!!!"""
    return 'Wow!!!!!'


def _get_image(data):
    """Get the image data from the data URL."""
    header, image_data = data['content']['data'].split(',')
    source = StringIO(base64.b64decode(image_data))
    image = Image.open(source)
    return image.convert('RGB')


def _downsample_image(image):
    """Returns a data URL of a crappy JPEG."""
    # Save the image at between 3 and 5 quality.
    dest = StringIO()
    image.save(dest, format='jpeg', quality=random.randrange(3, 6))

    # Base64 encode the image.
    dest.seek(0)
    encoded_data = base64.b64encode(dest.read())

    return 'data:image/jpeg;base64,' + encoded_data


@app.route('/service', methods=['POST'])
def service():
    """Returns a low quality version of an incoming image."""
    data = request.json

    image = _get_image(data)

    crappy_jpeg = _downsample_image(image)

    return jsonify({'content': {
        'data': crappy_jpeg,
    }})
