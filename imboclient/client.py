import requests

class Client:

    def __init__(self, server_urls, public_key, private_key, driver = None, version = None):
        self._server_urls = server_urls
        self._public_key = public_key
        self._private_key = private_key
        self._driver = driver
        self._version = version

    @property
    def server_urls(self):
        return self._server_urls

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
        class UrlImage:
            url = self._server_urls[0] + '/' + image_identifier;

        return UrlImage()

    def add_image(self, path):
        return

    def add_image_from_string(self, image):
        return

    def add_image_from_url(self, image):
        return

    def image_exists(self, path):
        return

    def image_identifier_exists(self, image_identifier):
        response = requests.get(self.image_url(image_identifier).url)
        return response.status_code == requests.codes.ok

    def head_image(self, image_identifier):
        return

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

    def image_identifier_from_string(self, image):
        return

    def server_status(self):
        return

    def user_info(self):
        return

