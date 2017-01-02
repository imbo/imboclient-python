from imboclient.url import accesstoken
from imboclient.url import url


class UrlImage (url.Url):
    def __init__(self, base_url, public_key, private_key, image_identifier, user=None):
        url.Url.__init__(self, base_url, public_key, private_key, user=user)
        self._image_identifier = image_identifier

    def resource_url(self):
        return self.user_url('images/' + self._image_identifier)

    def border(self, color='000000', width=1, height=1):
        self.add_query_param('t[]', "border:color={},width={},height={}".format(color, width, height))
        return self

    def compress(self, quality=75):
        self.add_query_param('t[]', "compress:quality={}".format(quality))
        return self

    def convert(self, ctype):
        self._image_identifier = self._image_identifier[:32] + '.' + ctype
        return self

    def gif(self):
        self.convert('gif')
        return self

    def jpg(self):
        self.convert('jpg')
        return self

    def png(self):
        self.convert('png')
        return self

    def crop(self, x, y, width, height):
        self.add_query_param('t[]', "crop:x={},y={},width={},height={}".format(x, y, width, height))
        return self

    def flip_horizontally(self):
        self.add_query_param('t[]', 'flipHorizontally')
        return self

    def flip_vertically(self):
        self.add_query_param('t[]', 'flipVertically')
        return self

    def resize(self, width=None, height=None):
        params = []

        if width:
            params.append('width='+str(width))

        if height:
            params.append('height='+str(height))

        self.add_query_param('t[]', 'resize:' + ",".join(params))

        return self

    def max_size(self, max_width=None, max_height=None):
        params = []

        if max_width:
            params.append('width='+str(max_width))

        if max_height:
            params.append('height='+str(max_height))

        self.add_query_param('t[]', 'maxSize:' + ",".join(params))

        return self

    def rotate(self, angle, bg='000000'):
        self.add_query_param('t[]', "rotate:angle={},bg={}".format(angle, bg))
        return self

    def thumbnail(self, width=50, height=50, fit='outbound'):
        self.add_query_param('t[]', "thumbnail:width={},height={},fit={}".format(width, height, fit))
        return self

    def canvas(self, width, height, mode=None, x=None, y=None, bg=None):
        self.add_query_param('t[]', "canvas:width={},height={},mode={},x={},y={},bg={}".format(width, height, mode, x, y, bg))
        return self

    def transpose(self):
        self.add_query_param('t[]', "transpose")
        return self

    def transverse(self):
        self.add_query_param('t[]', "transverse")
        return self

    def desaturate(self):
        self.add_query_param('t[]', "desaturate")
        return self

    def sepia(self, threshold=80):
        self.add_query_param('t[]', "sepia:threshold={}".format(threshold))
        return self

    def blur(self, type='gaussian', radius=5, sigma=2):
        self.add_query_param('t[]', "blur:type={},radius={},sigma={}".format(type, radius, sigma))
        return self

    def reset(self):
        url.Url.reset()
        self._image_identifier = self._image_identifier[:32]
        return self
