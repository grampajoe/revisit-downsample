import base64
from flask import json
from mock import patch
from PIL import Image
from StringIO import StringIO

from downsample import app


class TestApp(object):
    """Tests for the Flask app."""
    def setup_method(self, method):
        self.client = app.test_client()

        with open('tests/butt.jpg') as image:
            image_data = base64.b64encode(image.read())

        self.data = {
            'content': {
                'data': 'data:image/jpeg;base64,' + image_data,
            }
        }

    def _post_image(self):
        """POSTs an image to /service."""
        return self.client.post(
            '/service',
            data=json.dumps(self.data),
            content_type='application/json',
        )

    def test_get_index(self):
        """Should return a 200."""
        response = self.client.get('/')

        assert response.status_code == 200

    def test_post_service(self):
        """A POST to the /service endpoint should return a 200."""
        response = self._post_image()

        assert response.status_code == 200

    def test_service_returns_json(self):
        """/service should return JSON data."""
        response = self._post_image()

        assert response.headers['Content-Type'] == 'application/json'

    def test_service_returns_jpeg(self):
        """/service should return a jpeg image."""
        response = self._post_image()
        data = json.loads(response.data)

        assert data['content']['data'].startswith('data:image/jpeg;base64,')

    def test_service_returns_image_data(self):
        """/service should return real jpeg data!"""
        response = self._post_image()
        data = json.loads(response.data)
        header, image_data = data['content']['data'].split(',')
        image_file = StringIO(base64.b64decode(image_data))

        image = Image.open(image_file)

        assert image.format == 'JPEG'
        image.close()

    @patch('downsample.Image')
    def test_saves_low_quality(self, image_class):
        """The image should be saved at a low quality."""
        image = image_class.open.return_value
        image.convert.return_value = image

        self._post_image()

        args, kwargs = image.save.call_args

        assert kwargs['quality'] <= 5
        assert kwargs['quality'] >= 3

    @patch('downsample.Image')
    def test_converts_to_rgb(self, image_class):
        """Should convert all images into RGB."""
        image = image_class.open.return_value
        
        self._post_image()

        image.convert.assert_called_with('RGB')
