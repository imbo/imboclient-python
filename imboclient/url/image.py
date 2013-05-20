import accesstoken
import url

class UrlImage (url.Url):

    def __init__(self, base_url, public_key, private_key, image_identifier):
        url.Url.__init__(self, base_url, public_key, private_key)
        self._image_identifier = image_identifier

    def resource_url(self):
        return self._base_url + '/users/' + self._public_key + '/' + self._image_identifier

