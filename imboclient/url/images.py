from imboclient.url import accesstoken
from imboclient.url import url


class UrlImages (url.Url):
    def __init__(self, base_url, public_key, private_key):
        super(UrlImages, self).__init__(base_url, public_key, private_key)

    def resource_url(self):
        return self._base_url + '/users/' + self._public_key + '/images.json'
