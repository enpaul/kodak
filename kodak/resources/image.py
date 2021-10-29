from kodak.resources._shared import authenticated
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class Image(KodakResource):
    """Handle requests for original source images"""

    routes = ("/image/<string:image_name>",)

    @authenticated
    def get(self, image_name: str) -> ResponseTuple:
        """Retrieve an original source image"""
        raise NotImplementedError

    def head(self, image_name: str) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get(image_name))
