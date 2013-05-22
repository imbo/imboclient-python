from imboclient.url import url

class UrlStatus(url.Url):
    def resource_url(self):
        return self._base_url + '/users/' + self._public_key + '/status.json'

