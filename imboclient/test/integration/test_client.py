import imboclient.test.integration.config as config
import imboclient.client as imbo
import os

class TestClient:
    def setup(self):
        self._host = config.server['host']
        self._public = config.server['public']
        self._private = config.server['private']
        self._client = imbo.Client([self._host], self._public, self._private)
        self._res_path = os.path.dirname(__file__)

    def teardown(self):
        self._client = None

    def test_add_new_and_duplicate(self):
        result = self._client.add_image(self._res_path + '/res/imbologo.png')
        assert result.status_code == 201
        assert len(result.json()['imageIdentifier']) > 0

        result = self._client.add_image(self._res_path + '/res/imbologo.png')
        assert result.status_code == 200
        assert len(result.json()['imageIdentifier']) > 0

