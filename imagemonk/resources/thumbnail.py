import flask_restful


class ThumbnailScale(flask_restful.Resource):

    route = "/thumb/<string:image_id>/scale/<integer:scale_width>.jpg"

    def get(self, image_id: str, scale_width: int):
        raise NotImplementedError


class ThumbnailResize(flask_restful.Resource):

    route = "/thumb/<string:image_id>/size/<integer:width>x<integer:height>.jpg"

    def get(self, image_id: str, width: int, height: int):
        raise NotImplementedError
