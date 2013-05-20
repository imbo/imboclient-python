import accesstoken
import url

class UrlImages (url.Url):

    def resource_url(self):
        return self._base_url + '/users/' + self._public_key + '/images.json'
