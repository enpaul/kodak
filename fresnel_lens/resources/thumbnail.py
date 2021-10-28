from fresnel_lens.resources._shared import FresnelResource


class ThumbnailScale(FresnelResource):

    routes = ("/thumb/<string:image_id>/scale/<int:scale_width>.jpg",)

    def get(self, image_id: str, scale_width: int):
        raise NotImplementedError


class ThumbnailResize(FresnelResource):

    routes = ("/thumb/<string:image_id>/size/<int:width>x<int:height>.jpg",)

    def get(self, image_id: str, width: int, height: int):
        raise NotImplementedError
