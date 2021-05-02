from dehance.resources._shared import DehanceResource


class ThumbnailScale(DehanceResource):

    routes = ("/thumb/<string:image_id>/scale/<int:scale_width>.jpg",)

    def get(self, image_id: str, scale_width: int):
        raise NotImplementedError


class ThumbnailResize(DehanceResource):

    routes = ("/thumb/<string:image_id>/size/<int:width>x<int:height>.jpg",)

    def get(self, image_id: str, width: int, height: int):
        raise NotImplementedError
