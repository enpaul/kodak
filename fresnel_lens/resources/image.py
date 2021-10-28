import hashlib
import shutil
import uuid

import flask

from fresnel_lens import constants
from fresnel_lens import database
from fresnel_lens import exceptions
from fresnel_lens.resources._shared import FresnelResource


class ImageUpload(FresnelResource):

    routes = ("/image/",)

    def post(self):
        if "image" not in flask.request.files:
            raise

        uploaded = flask.request.files["image"]

        if not uploaded.filename:
            raise

        format = uploaded.filename.rpartition(".")[-1].lower()

        if format not in flask.current_app.appconfig.upload.formats:
            raise

        image = database.ImageRecord(format=format, width=0, height=0, owner="foobar")

        imagedir = flask.current_app.appconfig.storage_path / str(image.uuid)

        imagedir.mkdir()

        uploaded.save(imagedir / f"base.{format}")

        with (imagedir / f"base.{format}").open() as infile:
            image.sha256 = hashlib.sha256(infile.read()).hexdigest()

        with database.interface.atomic():
            image.save()

        return None, 201


class Image(FresnelResource):

    routes = ("/image/<string:image_id>.jpeg",)

    def get(self, image_id: str):

        image = database.ImageRecord.get(
            database.ImageRecord.uuid == uuid.UUID(image_id)
        )

        if image.deleted:
            raise exceptions.ImageResourceDeletedError(
                f"Image with ID '{image_id}' was deleted"
            )

        filepath = (
            flask.current_app.appconfig.storage_path
            / str(image.uuid)
            / f"base.{image.format}"
        )

        if not filepath.exists():
            with database.interface.atomic():
                image.deleted = True
                image.save()
            raise exceptions.ImageFileRemovedError(
                f"Image file with ID '{image_id}' removed from the server"
            )

        flask.send_file(
            filepath,
            mimetype=f"image/{'jpeg' if image.format == 'jpg' else image.format}",
            # images are indexed by UUID with no ability to update, y'all should cache
            # this thing 'till the sun explodes
            cache_timeout=(60 * 60 * 24 * 365),
        )

        return (
            None,
            200,
            {constants.HTTP_HEADER_RESPONSE_DIGEST: f"sha-256={image.sha256}"},
        )

    def delete(self, image_id: str, format: str):

        image = database.ImageRecord.get(
            database.ImageRecord.uuid
            == uuid.UUID(image_id) & database.ImageRecord.format
            == format
        )

        if image.deleted:
            raise exceptions.ImageResourceDeletedError(
                f"Image with ID '{image_id}' was deleted"
            )

        filepath = flask.current_app.appconfig.storage_path / str(image.uuid)

        with database.interface.atomic():
            image.deleted = True
            image.save()

        if filepath.exists():
            shutil.rmtree(filepath)

        return None, 204
