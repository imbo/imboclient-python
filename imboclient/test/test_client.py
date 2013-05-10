from mock import Mock
from mock import patch
from nose import with_setup
from imboclient import client as imbo
import requests

class TestClient:

    def setup(self):
        # before each test method
        self._client = imbo.Client(['imbo.local'], 'public', 'private');

    def teardown(self):
        # after each test method
        self._client = None

    @classmethod
    def setup_class(cls):
        # before class
        pass

    @classmethod
    def teardown_class(cls):
        # after class
        pass

    @patch('requests.get')
    def test_image_identifier_exists_true(self, mocked_requests_get):
        mocked_requests_get.return_value = self.valid_requests_response_stub_ok()

        assert self._client.image_identifier_exists('valididentifier') == True
        mocked_requests_get.assert_called_once_with('imbo.local/valididentifier')

    @patch('requests.get')
    def test_image_identifier_exists_false(self, mocked_requests_get):
        mocked_requests_get.return_value = self.invalid_requests_response_stub_not_found()

        assert self._client.image_identifier_exists('invalididentifier') == False
        mocked_requests_get.assert_called_once_with('imbo.local/invalididentifier')

    def valid_requests_response_stub_ok(self):
        class ResponseStub:
            status_code = requests.codes.ok

        return ResponseStub()

    def invalid_requests_response_stub_not_found(self):
        class ResponseStub:
            status_code = requests.codes.not_found

        return ResponseStub()

