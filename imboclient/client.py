import requests
import re
import os.path
import time
import hashlib
import json

from imboclient.header import authenticate
from imboclient.url import image
from imboclient.url import images
from imboclient.url import user as userUrl
from imboclient.url import status
from imboclient.url import metadata

py_version = 3

try:
    # py3
    from urllib.parse import urlparse
except ImportError:
    # py2
    from urlparse import urlparse
    py_version = 2

class Client:
    def __init__(self, server_urls, public_key, private_key, version=None, user=None):
        self.server_urls = self._parse_urls(server_urls)
        self._public_key = public_key
        self._private_key = private_key
        self._version = version
        self._user = user

    def metadata_url(self, image_identifier):
        return metadata.UrlMetadata(self._pick_url(image_identifier), self._public_key, self._private_key, image_identifier, user=self._user)

    def status_url(self):
        return status.UrlStatus(self._pick_url(), self._public_key, self._private_key)

    def user_url(self):
        return userUrl.UrlUser(self._pick_url(), self._public_key, self._private_key)

    def images_url(self):
        return images.UrlImages(self._pick_url(), self._public_key, self._private_key, user=self._user)

    def image_url(self, image_identifier):
        return image.UrlImage(self._pick_url(image_identifier), self._public_key, self._private_key, image_identifier, user=self._user)

    def add_image(self, path):
        image_file_data = self._image_file_data(path)

        url = self.images_url().url()
        headers = self._auth_headers('POST', url)

        def http_add_image(self):
            return requests.post(url, data=image_file_data,  headers=headers)

        return self._wrap_result_json(http_add_image, [200, 201], 'Could not add image.')

    def add_image_from_string(self, image):
        image_url = self.images_url().url()
        headers = self._auth_headers('POST', image_url)

        def http_add_image_from_string(self):
            return requests.post(image_url, data=image, headers=headers)

        return self._wrap_result_json(http_add_image_from_string, [200, 201], 'Could not add image.')

    def add_image_from_url(self, image_url):
        def http_add_image_from_url(self):
            return requests.get(image_url)

        image_string = self._wrap_result(http_add_image_from_url, [200], 'Could not get fetch image data to add').content

        return self.add_image_from_string(image_string)

    def image_exists(self, imbo_id):
        return self.image_identifier_exists(imbo_id)

    def image_identifier_exists(self, image_identifier):
        result = self.head_image(image_identifier)
        return result.status_code == requests.codes.ok

    def head_image(self, image_identifier):
        def http_head_image(self):
            return requests.head(self.image_url(image_identifier).url())

        return self._wrap_result(http_head_image, [200, 404], 'Could not get image headers.')

    def delete_image(self, image_identifier):
        delete_url = self.image_url(image_identifier).url()
        headers = self._auth_headers('DELETE', delete_url)

        def http_delete_image(self):
            return requests.delete(delete_url, headers = headers)

        return self._wrap_result_json(http_delete_image, [200, 404], 'Could not delete image.')

    def edit_metadata(self, image_identifier, metadata):
        edit_metadata_url = self.metadata_url(image_identifier).url()
        metadata = json.dumps(metadata).encode('utf-8')
        headers = self._auth_headers('POST', edit_metadata_url)

        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        headers['Content-MD5'] = hashlib.md5(metadata).hexdigest()

        def http_edit_metadata(self):
            return requests.post(edit_metadata_url, data=metadata, headers=headers)

        return self._wrap_result_json(http_edit_metadata, [200], 'Could not edit metadata.')

    def replace_metadata(self, image_identifier, metadata):
        replace_metadata_url = self.metadata_url(image_identifier).url()
        metadata = json.dumps(metadata).encode('utf-8')
        headers = self._auth_headers('PUT', replace_metadata_url)

        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'
        headers['Content-MD5'] = hashlib.md5(metadata).hexdigest()

        def http_replace_metadata(self):
            return requests.put(replace_metadata_url, data=metadata, headers=headers)

        return self._wrap_result_json(http_replace_metadata, [200], 'Could not replace metadata.')

    def delete_metadata(self, image_identifier):
        delete_metadata_url = self.metadata_url(image_identifier).url()
        headers = self._auth_headers('DELETE', delete_metadata_url)

        def http_delete_metadata(self):
            return requests.delete(delete_metadata_url, headers=headers)

        return self._wrap_result_json(http_delete_metadata, [200], 'Could not delete metadata.')

    def num_images(self):
        user_url = self.user_url().url()

        def http_num_images(self):
            return requests.get(user_url, headers={'Accept': 'application/json'})

        user_data_decoded = self._wrap_result_json(http_num_images, [200], 'Could not get number of images.')

        try:
            return user_data_decoded['numImages']
        except KeyError as error:
            raise self.ImboInternalError(str(error) + ' Could not extract number of images from Imbo response.')

    def images(self, query = None):
        images_url = images.UrlImages(self._pick_url(), self._public_key, self._private_key)

        if query:
            images_url.add_query(query)

        def http_images(self):
            return requests.get(images_url.url(), headers={'Accept': 'application/json'})

        return self._wrap_result_json(http_images, [200], 'Could not get images.')

    def image_data(self, image_identifier):
        image_url = self.image_url(image_identifier).url()
        return self.image_data_from_url(image_url)

    def image_data_from_url(self, url):
        def http_image_data(self):
            return requests.get(url)

        return self._wrap_result(http_image_data, [200], 'Could not get image data.')

    def image_properties(self, image_identifier):
        headers = self.head_image(image_identifier).headers

        try:
            return {
                    "x-imbo-originalwidth": headers['x-imbo-originalwidth'],
                    "x-imbo-originalheight": headers["x-imbo-originalheight"],
                    "x-imbo-originalfilesize": headers["x-imbo-originalfilesize"],
                    "x-imbo-originalmimetype": headers["x-imbo-originalmimetype"],
                    "x-imbo-originalextension": headers["x-imbo-originalextension"]
                    }
        except KeyError as key_error:
            raise self.ImboInternalError(str(key_error) + ' Imbo failed returning image properties.')

    def image_identifier(self, path):
        if self._validate_local_file(path):
            return self._generate_image_identifier(open(path, 'rb').read())

        raise ValueError("Either the path is invalid or empty file")

    def image_identifier_from_string(self, image):
        return self._generate_image_identifier(image)

    def server_status(self):
        url = self.status_url().url()

        def http_server_status(self):
            return requests.get(url, headers={'Accept': 'application/json'})

        return self._wrap_result_json(http_server_status, [200], 'Failed getting server status.')

    def user_info(self):
        url = self.user_url().url()

        def http_user_info(self):
            return requests.get(url, headers={'Accept': 'application/json'})

        return self._wrap_result_json(http_user_info, [200], 'Failed getting user info.')

    def _pick_url(self, key=None):
        if key:
            return self.server_urls[ord(key[0]) % len(self.server_urls)]
        else:
            return self.server_urls[0]

    def _parse_urls(self, urls):
        def should_remove_port(self, url_parts):
            return url_parts.port and (url_parts.scheme == 'http' and url_parts.port == 80 or (url_parts.scheme == 'https' and url_parts.port == 443))

        parsed_urls = []
        pattern = re.compile("https?://")

        if isinstance(urls, str) or (py_version == 2 and isinstance(urls, basestring)):
            urls = [urls]

        for url in urls:
            if not pattern.match(url):
                url = 'http://' + url

            parts = urlparse(url)

            if should_remove_port(self, parts):
                url = parts.scheme + '://' + parts.hostname + '/' + parts.path

            parsed_urls.append(url.rstrip('/'))

        return parsed_urls

    def _auth_headers(self, method, url):
        return authenticate.Authenticate(self._public_key, self._private_key, method, url, self._current_timestamp()).headers()

    def _wrap_result_json(self, function, success_status_codes, error):
        response = self._wrap_result(function, success_status_codes, error)

        try:
            response_json = response.json()
        except ValueError as value_error:
            raise self.ImboInternalError(error + ' The response from Imbo could not be parsed as JSON: \'' + response.text + '\'')

        return response_json

    def _wrap_result(self, function, success_status_codes, error):
        try:
            response = function(self)
        except requests.exceptions.RequestException as request_error:
            raise self.ImboTransportError(error + ', HTTP library returned error: ' + str(request_error))

        if response.status_code in success_status_codes:
            return response
        else:
            raise self.ImboInternalError(error + ' Imbo returned HTTP ' + str(response.status_code) + ' and body \'' + response.text + '\'')

    @classmethod
    def _current_timestamp(cls):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @classmethod
    def _generate_image_identifier(cls, content):
        return hashlib.md5(content).hexdigest()

    @classmethod
    def _image_file_data(cls, path):
        return open(path, 'rb').read()

    @classmethod
    def _validate_local_file(cls, path):
        return os.path.isfile(path) and os.path.getsize(path) > 0

    class ImboTransportError(Exception):
       pass

    class ImboInternalError(Exception):
       pass

