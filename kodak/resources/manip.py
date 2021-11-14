from kodak.resources._shared import authenticated
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class ImageManip(KodakResource):
    """Handle generating and returning a processed image manip"""

    routes = ("/image/<string:image_name>/<string:manip>",)

    @authenticated
    def get(self, image_name: str, manip: str) -> ResponseTuple:
        """Retrieve an image variation"""
        raise NotImplementedError

    def head(self, image_name: str, manip: str) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get(image_name, manip))
