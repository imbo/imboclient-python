import requests
import re
import urlparse
import hmac, hashlib
import url.image

class Client:

    def __init__(self, server_urls, public_key, private_key, driver = None, version = None):
        self.server_urls = self._parse_urls(server_urls)
        self._public_key = public_key
        self._private_key = private_key
        self._driver = driver
        self._version = version

    @property
    def driver(self, value):
        self._driver = value

    @property
    def status_url(self):
        return self._status_url

    @property
    def user_url(self):
        return self._user_url

    @property
    def images_url(self):
        return self._images_url

    @property
    def metadata(self):
        return self._metadata;

    @property
    def metadata_url(self, image_identifier):
        return

    def image_url(self, image_identifier):
        host = self._host_for_image_identifier(image_identifier)
        return url.image.UrlImage(host, self._public_key, self._private_key, image_identifier)

    def add_image(self, path):
        return

    def add_image_from_string(self, image):
        return

    def add_image_from_url(self, image):
        return

    def image_exists(self, path):
        return

    def image_identifier_exists(self, image_identifier):
        result = self.head_image(image_identifier)
        return result.status_code == requests.codes.ok

    def head_image(self, image_identifier):
        response = requests.head(self.image_url(image_identifier).url)
        return response

    def delete_image(self, image_identifier):
        return

    def edit_metadata(self, image_identifier, metadata):
        return

    def replace_metadata(self, image_identifier, metadata):
        return

    def delete_metadata(self, image_identifier):
        return

    def num_images(self):
        return

    def images(self, query):
        return

    def image_data(self, image_identifier):
        return

    def image_data_from_url(self, url):
        return

    def image_properties_from_url(self, url):
        return

    def image_properties(self, image_identifier):
        return

    def image_identifier(self, path):
        return

    def _host_for_image_identifier(self, image_identifier):
        dec = int(image_identifier[0] + image_identifier[1], 16)
        return self.server_urls[dec % len(self.server_urls)]

    def image_identifier_from_string(self, image):
        return

    def server_status(self):
        return

    def user_info(self):
        return

    def _parse_urls(self, urls):
        def should_remove_port(self, url_parts):
            return parts.port and (parts.scheme == 'http' and parts.port == 80 or (parts.scheme == 'https' and parts.port == 443))

        parsed_urls = []
        pattern = re.compile("https?://")

        for url in urls:
            if not pattern.match(url):
                parsed_urls.append('http://' + url)

            parts = urlparse.urlparse(url)

            if should_remove_port(self, parts):
                url = parts.scheme + '://' + parts.hostname + '/' + parts.path

            parsed_urls.append(url.rstrip('/'))

        return parsed_urls

    def _generate_signature(self, method, url, timestamp):
        data = method + '|' + url + '|' + self._public_key + '|' + timestamp
        return hmac.new(self._private_key, data, hashlib.sha256).hexdigest()

    def _signed_url (self, method, url):
        def first_delimeter():
            if url.find('?'):
                return '&'
            else:
                return '?'

        timestamp = gmdate('Y-m-d\TH:i:s\Z')
        signature = self._generate_signature(method, url, timestamp)

        return sprintf('%s%ssignature=%s&timestamp=%s', url, first_delimeter(), signature, timestamp)

    class ParsedUrl:
        def __init__(self, scheme, host, port):
            self.scheme = scheme
            self.host = host
            self.port = port


