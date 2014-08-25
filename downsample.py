import base64
import random
from flask import Flask, jsonify, request
from PIL import Image
from StringIO import StringIO
from werkzeug.exceptions import BadRequest


app = Flask('downsample')


@app.route('/')
def index():
    """Returns a 200, that's about it!!!!!!!"""
    return 'Wow!!!!!'


def _validate(data):
    """Validates that the provided JSON is okey-dokey."""
    if not 'content' in data:
        raise BadRequest('Invalid JSON: No content attribute found.')
    elif not 'data' in data['content']:
        raise BadRequest('Invalid JSON: No image data found.')
    elif not isinstance(data['content']['data'], basestring):
        raise BadRequest('Image data must be a string.')


def _get_image(data_url):
    """Get the image data from the data URL."""
    if not data_url.startswith('data') or not ',' in data_url:
        raise BadRequest('No data URL found.')

    header, image_data = data_url.split(',')

    try:
        decoded_data = base64.b64decode(image_data)
    except TypeError:
        raise BadRequest('Image data was not base64.')

    source = StringIO(decoded_data)

    try:
        image = Image.open(source)
    except IOError:
        raise BadRequest('Invalid image data.')

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
    _validate(data)

    image = _get_image(data['content']['data'])

    crappy_jpeg = _downsample_image(image)

    return jsonify({'content': {
        'data': crappy_jpeg,
    }})
