from fresnel_lens.resources._shared import FresnelResource
from fresnel_lens.resources._shared import ResponseTuple


class ImageAlias(FresnelResource):

    routes = ("/image/<string:image_name>/<string:alias>",)

    def get(self, image_name: str, alias: str) -> ResponseTuple:
        raise NotImplementedError
