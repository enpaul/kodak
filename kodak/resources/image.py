import datetime

import flask

from kodak import database
from kodak.resources._shared import authenticated
from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple


class Image(KodakResource):
    """Handle requests for original source images"""

    routes = ("/image/<string:image_name>/original",)

    @authenticated
    def get(self, image_name: str) -> flask.Response:  # pylint: disable=no-self-use
        """Retrieve an original source image"""
        if not flask.current_app.appconfig.expose_source:
            raise RuntimeError

        with database.interface.atomic():
            image = database.ImageRecord.get(database.ImageRecord.name == image_name)

        # Note that this sends the original source file directly, rather than the symlink named
        # "original". This is because flask will serve the symlink file itself, not the linked file,
        # to the browser.
        resp = flask.send_file(
            flask.current_app.appconfig.source_dir / image.source,
            cache_timeout=int(datetime.timedelta(days=365).total_seconds()),
            add_etags=False,
        )

        resp.headers["Content-Digest"] = image.checksum.as_header()

        return resp

    def head(self, image_name: str) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get(image_name))
