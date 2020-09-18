import flask_restful


class ImageUpload(flask_restful.Resource):

    route = "/image/"

    def put(self):
        raise NotImplementedError

    def options(self):
        raise NotImplementedError


class Image(flask_restful.Resource):

    route = "/image/<string:image_id>.jpg"

    def get(self, image_id: str):
        raise NotImplementedError

    def delete(self, image_id: str):
        raise NotImplementedError

    def options(self, image_id: str):
        raise NotImplementedError
