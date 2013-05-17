from mock import Mock
from mock import patch
from nose import with_setup
from imboclient import client as imbo
import requests

class TestClient:
    # valid md5 hash
    _valid_image_identifier = 'ffffffffffffffffffffffffffffffff'

    # externally pre-calculated sha256 hashes of GET requests used for testing
    _valid_get_request_tokens = {
                'http://imbo.local/users/public/' + _valid_image_identifier: 'b86400becdaacbedf74f22c8d53b59d4bf8519fe6e75abdc1f0c84e9465a0169'
                }

    def setup(self):
        # before each test method
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');

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

    def test_server_urls_generic(self):
        self._client = imbo.Client(['imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_http(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_https(self):
        self._client = imbo.Client(['https://imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'https://imbo.local'

    def test_server_urls_port_normal(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_port_normal_explicit(self):
        self._client = imbo.Client(['http://imbo.local:80'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_port_ssl(self):
        self._client = imbo.Client(['https://imbo.local:443'], 'public', 'private');
        assert self._client.server_urls[0] == 'https://imbo.local'

    def test_server_urls_port_explicit_without_protocol(self):
        self._client = imbo.Client(['imbo.local:8000'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local:8000'

    def test_image_url(self):
        valid_image_url = 'http://imbo.local/users/public/' + self._valid_image_identifier
        token_for_valid_image_url = self._valid_get_request_tokens[valid_image_url]
        valid_image_url = valid_image_url + '?accessToken=' + token_for_valid_image_url
        assert str(self._client.image_url(self._valid_image_identifier)) == valid_image_url

    @patch('requests.head')
    def test_image_identifier_exists_true(self, mocked_requests_get):
        mocked_requests_get.return_value = self._valid_requests_response_stub_ok()

        assert self._client.image_identifier_exists(self._valid_image_identifier) == True
        request_url = self._sign_test_request('http://imbo.local/users/public/' + self._valid_image_identifier)
        mocked_requests_get.assert_called_once_with(request_url)

    @patch('requests.head')
    def test_image_identifier_exists_false(self, mocked_requests_get):
        mocked_requests_get.return_value = self._invalid_requests_response_stub_not_found()

        assert self._client.image_identifier_exists(self._valid_image_identifier) == False
        request_url = self._sign_test_request('http://imbo.local/users/public/' + self._valid_image_identifier)
        mocked_requests_get.assert_called_once_with(request_url)

    def _valid_requests_response_stub_ok(self):
        class ResponseStub:
            status_code = requests.codes.ok

        return ResponseStub()

    def _invalid_requests_response_stub_not_found(self):
        class ResponseStub:
            status_code = requests.codes.not_found

        return ResponseStub()

    def _sign_test_request(self, url):
        request_token = self._valid_get_request_tokens[url]
        return url + '?accessToken=' + request_token

