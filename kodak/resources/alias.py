from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class ImageAlias(KodakResource):

    routes = ("/image/<string:image_name>/<string:alias>",)

    def get(self, image_name: str, alias: str) -> ResponseTuple:
        raise NotImplementedError
