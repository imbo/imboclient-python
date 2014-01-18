import imboclient.test.integration.config as config
import imboclient.client as imbo

class TestClient:
    def setup(self):
        self._host = config.server['host']
        self._public = config.server['public']
        self._private = config.server['private']
        self._client = imbo.Client([self._host], self._public, self._private)

    def teardown(self):
        self._client = None

    def test_add_image(self):
        result = self._client.add_image('res/imbologo.png')
        print result

