from kodak.resources._shared import authenticated
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class ImageAlias(KodakResource):
    """Handle generating and returning a processed image alias"""

    routes = ("/image/<string:image_name>/<string:alias>",)

    @authenticated
    def get(self, image_name: str, alias: str) -> ResponseTuple:
        """Retrieve an image variation"""
        raise NotImplementedError

    def head(self, image_name: str, alias: str) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get(image_name, alias))
