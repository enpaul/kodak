from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class Image(KodakResource):

    routes = ("/image/<string:image_name>",)

    def get(self, image_name: str) -> ResponseTuple:
        raise NotImplementedError
