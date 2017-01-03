from imboclient.url import accesstoken
from imboclient.url import url


class UrlImages (url.Url):
    def __init__(self, base_url, public_key, private_key, user=None):
        super(UrlImages, self).__init__(base_url, public_key, private_key, user=user)

    def resource_url(self):
        return self.user_url('images.json')
