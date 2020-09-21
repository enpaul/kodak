from imagemonk.resources._shared import ImageMonkResource


class ImageUpload(ImageMonkResource):

    route = ("/image/",)

    def post(self):
        raise NotImplementedError


class Image(ImageMonkResource):

    route = ("/image/<string:image_id>.jpg",)

    def get(self, image_id: str):
        raise NotImplementedError

    def delete(self, image_id: str):
        raise NotImplementedError
