from mock import patch
from mock import MagicMock
from nose import with_setup
from nose.tools import raises
import requests
import os
import json
import hashlib
from imboclient import client as imbo
from imboclient.url import image, images, status, user, accesstoken, metadata
import __builtin__

class TestClient:

    def setup(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');

    def teardown(self):
        self._client = None

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

    @patch('imboclient.url.status.UrlStatus')
    def test_status_url(self, mocked_url_status):
        status_url = self._client.status_url()
        mocked_url_status.assert_called_once_with('http://imbo.local', 'public', 'private')
        assert status_url == mocked_url_status()

    @patch('imboclient.url.user.UrlUser')
    def test_user_url(self, mocked_url_user):
        user_url = self._client.user_url()
        mocked_url_user.assert_called_once_with('http://imbo.local', 'public', 'private')
        assert user_url == mocked_url_user()

    @patch('imboclient.url.images.UrlImages')
    def test_images_url(self, mocked_url_images):
        images_url = self._client.images_url()
        mocked_url_images.assert_called_once_with('http://imbo.local', 'public', 'private')
        assert images_url == mocked_url_images()

    @patch('imboclient.url.image.UrlImage')
    def test_image_url(self, mocked_url_image):
        image_url = self._client.image_url('ff')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff')
        assert image_url == mocked_url_image()

    @patch('imboclient.url.metadata.UrlMetadata')
    def test_metadata_url(self, mocked_url_metadata):
        metadata_url = self._client.metadata_url('ff')
        mocked_url_metadata.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff')
        assert metadata_url == mocked_url_metadata()

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.images.UrlImages.url')
    @patch('requests.post')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    def test_add_image(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile, mocked_requests_post, mocked_url, mocked_headers):
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 7

        mocked_url.return_value = 'url'
        mocked_headers.return_value = {'Accept': 'application/json'}

        result = self._client.add_image('/mocked/image/path.jpg')
        mocked_requests_post.assert_called_once_with('url', data = 'content', headers = {'Accept': 'application/json'})

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('requests.post')
    @patch('imboclient.url.images.UrlImages.url')
    def test_add_image_from_string(self, mock_image_url, mock_requests_post, mock_headers):
        mock_image_url.return_value = 'imageurl'
        mock_headers.return_value = {'Accept': 'application/json'}

        result = self._client.add_image_from_string('imagestring')

        mock_requests_post.assert_called_once_with('imageurl', data = 'imagestring', headers = {'Accept': 'application/json'})
        assert result

    @patch('imboclient.client.Client.add_image_from_string')
    @patch('requests.get')
    def test_add_image_from_url(self, mock_requests_get, mock_add_image_from_string):
        mock_requests_get.return_value = 'imagedatafromhttp'

        self._client.add_image_from_url('validimageurl')
        mock_requests_get.assert_called_once_with('validimageurl')
        mock_add_image_from_string.assert_called_once_with('imagedatafromhttp')

    @patch('imboclient.client.Client.image_identifier')
    @patch('imboclient.client.Client.image_identifier_exists')
    def test_image_exists(self, mock_image_identifier_exists, mock_image_identifier):
        mock_image_identifier.return_value = 'identifier'
        mock_image_identifier_exists.return_value = True

        image_exists = self._client.image_exists('/dummy/path')

        assert image_exists == True
        mock_image_identifier_exists.assert_called_once_with('identifier')
        mock_image_identifier.assert_called_once_with('/dummy/path')

    @patch('requests.head')
    @patch('imboclient.url.image.UrlImage')
    def test_image_identifier_exists_true(self, mocked_url_image, mocked_requests_head) :
        mocked_requests_head.return_value = self._valid_requests_response_stub_ok()
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'http://imbo.local/users/public/ff?accessToken=aa'

        assert self._client.image_identifier_exists('ff') == True
        mocked_requests_head.assert_called_once_with('http://imbo.local/users/public/ff?accessToken=aa')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff')

    @patch('requests.head')
    @patch('imboclient.url.image.UrlImage')
    def test_image_identifier_exists_false(self, mocked_url_image, mocked_requests_get):
        mocked_requests_get.return_value = self._invalid_requests_response_stub_not_found()
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'http://imbo.local/users/public/ffa?accessToken=aaf'

        assert self._client.image_identifier_exists('ffa') == False
        mocked_requests_get.assert_called_once_with('http://imbo.local/users/public/ffa?accessToken=aaf')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ffa')

    @patch('imboclient.url.image.UrlImage.url')
    @patch('requests.head')
    def test_head_image(self, mock_requests_head, mock_image_url):
        mock_image_url.return_value = "imageurl"
        self._client.head_image("ff")
        mock_image_url.assert_called_once_with()
        mock_requests_head.assert_called_once_with("imageurl")

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.image.UrlImage.url')
    @patch('requests.delete')
    def test_delete_image(self, mock_requests_delete, mock_image_url, mock_headers):
        mock_image_url.return_value = "imageurl"
        mock_headers.return_value = {}
        self._client.delete_image("imageidentifier")
        mock_image_url.assert_called_once_with()
        mock_requests_delete.assert_called_once_with("imageurl", headers = {})

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.metadata.UrlMetadata.url')
    @patch('requests.post')
    def test_edit_metadata(self, mock_requests_post, mock_metadata_url, mock_headers):
        mock_metadata_url.return_value = 'metadataurl'
        mock_headers.return_value = {}

        metadata = {"field1": "value1", "field2": "value2"}
        self._client.edit_metadata('identifier', metadata)
        metadata = json.dumps(metadata)

        mock_requests_post.assert_called_once_with('metadataurl', data = metadata, headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Content-Length': len(metadata), 'Content-MD5': hashlib.md5(metadata).hexdigest()})

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.metadata.UrlMetadata.url')
    @patch('requests.put')
    def test_replace_metadata(self, mock_requests_put, mock_metadata_url, mock_headers):
        mock_metadata_url.return_value = 'metadataurl'
        mock_headers.return_value = {}

        metadata = {"field1": "value1", "field2": "value2"}
        self._client.replace_metadata('identifier', metadata)
        metadata = json.dumps(metadata)

        mock_requests_put.assert_called_once_with('metadataurl', data = metadata, headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Content-Length': len(metadata), 'Content-MD5': hashlib.md5(metadata).hexdigest()})

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.metadata.UrlMetadata.url')
    @patch('requests.delete')
    def test_delete_metadata(self, mock_requests_delete, mock_metadata_url, mock_headers):
        mock_metadata_url.return_value = 'metadataurl'
        mock_headers.return_value = {'Accept': 'application/json'}

        self._client.delete_metadata('identifier')

        mock_requests_delete.assert_called_once_with('metadataurl', headers = {'Accept': 'application/json'})

    @patch('requests.get')
    @patch('imboclient.url.user.UrlUser.url')
    def test_num_images(self, mocked_url_user, mocked_requests_get):
        class StubResponse:
            text = '{"numImages": 2}'

        mocked_url_user.return_value = 'http://imbo.local/users/public'
        mocked_requests_get.return_value = StubResponse()

        num_images = self._client.num_images()

        mocked_url_user.assert_called_once_with()
        mocked_requests_get.assert_called_once_with(mocked_url_user.return_value, headers = {'Accept': 'application/json'})

        assert num_images == 2

    @patch('imboclient.url.imagesquery.Query')
    @patch('imboclient.url.images.UrlImages.url')
    @patch('imboclient.url.images.UrlImages.add_query')
    @patch('requests.get')
    def test_images(self, mock_requests_get, mock_url_images_addquery, mock_url_images, mock_imagesquery):
        class StubResponse:
            text = '[{"key": "value"}]'

        mock_url_images.return_value = 'http://imbo.local/public/images.json'
        mock_requests_get.return_value = StubResponse()

        images = self._client.images(mock_imagesquery)
        assert len(images) == 1

        mock_requests_get.assert_called_once_with(mock_url_images.return_value, headers = {'Accept': 'application/json'})
        mock_url_images_addquery.assert_called_once_with(mock_imagesquery)

    @patch('imboclient.url.image.UrlImage.url')
    @patch('imboclient.client.Client.image_data_from_url')
    def test_image_data(self, mock_image_data_from_url, mock_image_url):
        mock_image_data_from_url.return_value = 'data'
        mock_image_url.return_value = 'validimageurl'

        image_data = self._client.image_data('ff')
        mock_image_data_from_url.assert_called_once_with('validimageurl')
        assert image_data == 'data'

    @patch('requests.get')
    def test_image_data_from_url(self, mock_requests_get):
        class ResponseStub:
            text = 'data'

        mock_requests_get.return_value = ResponseStub()
        image_data = self._client.image_data_from_url('validurl')
        mock_requests_get.assert_called_once_with('validurl')

        assert image_data.text == 'data'

    @patch('imboclient.client.Client.head_image')
    def test_image_properties(self, mock_head_image):
        class ResponseStub:
            headers = {
                    "x-imbo-originalwidth": "width",
                    "x-imbo-originalheight": "height",
                    "x-imbo-originalfilesize": "size",
                    "x-imbo-originalmimetype": "mime",
                    "x-imbo-originalextension": "ext"
                    }

        mock_head_image.return_value = ResponseStub()

        image_properties = self._client.image_properties('ff')
        assert image_properties["x-imbo-originalwidth"] == 'width'
        assert image_properties["x-imbo-originalheight"] == 'height'
        assert image_properties["x-imbo-originalfilesize"] == 'size'
        assert image_properties["x-imbo-originalmimetype"] == 'mime'
        assert image_properties["x-imbo-originalextension"] == 'ext'

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    def test_image_identifier(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile):
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 7

        assert self._client.image_identifier('/path/to/file') == '9a0364b9e99bb480dd25e1f0284c8555'
        mocked_os_path_isfile.assert_called_once_with('/path/to/file')
        mocked_os_path_getsize.assert_called_once_with('/path/to/file')

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    @raises(ValueError)
    def test_image_identifier_no_file(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile):
        # TODO it would be better to move file related actions to a separately tested module
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = False
        mocked_os_path_getsize.return_value = 0

        self._client.image_identifier('/dev/null/invalid')
        mocked_os_path_isfile.assert_called_once_with('/dev/null/invalid')

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    @raises(ValueError)
    def test_image_identifier_empty_file(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile):
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 0

        self._client.image_identifier('/dev/null/invalid')
        mocked_os_path_getsize.assert_called_once_with('/dev/null/invalid')

    @patch('imboclient.client.Client._generate_image_identifier')
    def test_image_identifier_from_string(self, mock_generate_image_identifier):
        self._client.image_identifier_from_string('imagestring')
        mock_generate_image_identifier.assert_called_once_with('imagestring')

    @patch('imboclient.url.status.UrlStatus.url')
    @patch('requests.get')
    def test_server_status(self, mocked_requests_get, mocked_url_status):
        class ResponseStub:
            text = '{"statusKey": "statusValue"}'

        mocked_url_status.return_value = 'http://imbo.local/status.json'
        mocked_requests_get.return_value = ResponseStub()

        server_status = self._client.server_status()

        assert server_status['statusKey'] == 'statusValue'
        mocked_url_status.assert_called_once_with()
        mocked_requests_get.assert_called_once_with(mocked_url_status.return_value, headers = {'Accept': 'application/json'})

    @patch('imboclient.url.user.UrlUser.url')
    @patch('requests.get')
    def test_user_info(self, mocked_requests_get, mocked_url_user):
        class ResponseStub:
            text = '{"public": "publickey"}'

        mocked_requests_get.return_value = ResponseStub()
        mocked_url_user.return_value = 'http://imbo.local/users/public'

        user_info = self._client.user_info()
        assert user_info['public'] == 'publickey'

        mocked_url_user.assert_called_once_with()
        mocked_requests_get.assert_called_once_with(mocked_url_user.return_value, headers = {'Accept': 'application/json'})

    def _valid_requests_response_stub_ok(self):
        class ResponseStub:
            status_code = requests.codes.ok

        return ResponseStub()

    def _invalid_requests_response_stub_not_found(self):
        class ResponseStub:
            status_code = requests.codes.not_found

        return ResponseStub()

