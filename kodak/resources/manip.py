import datetime

import flask
import peewee

from kodak import constants
from kodak import database
from kodak.resources._shared import authenticated
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class ImageManip(KodakResource):
    """Handle generating and returning a processed image manip"""

    routes = ("/image/<string:image_name>/<string:manip_name>.<string:format_name>",)

    @authenticated
    def get(  # pylint: disable=no-self-use
        self, image_name: str, manip_name: str, format_name: str
    ) -> flask.Response:
        """Retrieve an image variation"""
        try:
            manip_config = flask.current_app.appconfig.manips[manip_name]
            format_ = constants.ImageFormat[format_name.upper()]
        except KeyError:
            raise RuntimeError("Manip or format doesn't exist") from None

        with database.interface.atomic():
            parent = database.ImageRecord.get(database.ImageRecord.name == image_name)

            try:
                manip = (
                    database.ManipRecord.select()
                    .where(
                        database.ManipRecord.parent == parent,
                        database.ManipRecord.name == manip_config.name,
                        database.ManipRecord.format_ == format_,
                    )
                    .get()
                )
            except peewee.DoesNotExist:
                manip = database.ManipRecord.from_parent(
                    parent, flask.current_app.appconfig, manip_config, format_
                )

        resp = flask.send_file(
            (flask.current_app.appconfig.content_dir / manip.file),
            cache_timeout=int(datetime.timedelta(days=365).total_seconds()),
            add_etags=False,
        )

        resp.headers["Content-Digest"] = manip.checksum.as_header()

        return resp

    def head(self, image_name: str, manip_name: str, format_name: str) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get(image_name, manip_name, format_name))
