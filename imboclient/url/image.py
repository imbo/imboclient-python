from imboclient.url import accesstoken
from imboclient.url import url

class UrlImage (url.Url):

    def __init__(self, base_url, public_key, private_key, image_identifier):
        url.Url.__init__(self, base_url, public_key, private_key)
        self._image_identifier = image_identifier

    def resource_url(self):
        return self._base_url + '/users/' + self._public_key + '/' + self._image_identifier

    def border(self, color = '000000', width = 1, height = 1):
        return

    def compress(self, quality = 75):
        return

    def convert(self, ctype):
        return

    def gif(self):
        return

    def jpg(self):
        return

    def png(self):
        return

    def crop(self, x, y, width, height):
        return

    def flip_horizontally(self):
        return

    def flip_vertically(self):
        return

    def resize(self, width, height):
        return

    def max_size(self, max_width, max_height):
        return

    def rotate(self, angle, bg = '000000'):
        return

    def thumbnail(self, width = 50, height = 50, fit = 'outbound'):
        return

    def canvas(self, width, height, mode = None, x = None, y = None, bg = None):
        return

    def transponse(self):
        return

    def transverse(self):
        return

    def desaturate(self):
        return
