from fresnel_lens.resources._shared import FresnelResource
from fresnel_lens.resources._shared import ResponseTuple


class Image(FresnelResource):

    routes = ("/image/<string:image_name>",)

    def get(self, image_name: str) -> ResponseTuple:
        raise NotImplementedError
