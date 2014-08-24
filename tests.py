from downsample import app


class TestApp(object):
    """Tests for the Flask app."""
    def setup_method(self, method):
        self.client = app.test_client()

    def test_get_index(self):
        """Should return a 200."""
        response = self.client.get('/')

        assert response.status_code == 200
