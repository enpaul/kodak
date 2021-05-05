from imagemuck.resources._shared import ImageMuckResource


class ThumbnailScale(ImageMuckResource):

    routes = ("/thumb/<string:image_id>/scale/<int:scale_width>.jpg",)

    def get(self, image_id: str, scale_width: int):
        raise NotImplementedError


class ThumbnailResize(ImageMuckResource):

    routes = ("/thumb/<string:image_id>/size/<int:width>x<int:height>.jpg",)

    def get(self, image_id: str, width: int, height: int):
        raise NotImplementedError
