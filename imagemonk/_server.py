import flask

from imagemonk import __about__
from imagemonk import configuration
from imagemonk import constants
from imagemonk import database
from imagemonk import exceptions
from imagemonk.resources import ResponseHeaders


def make_the_tea() -> None:
    """Just for fun
    https://en.wikipedia.org/wiki/Hyper_Text_Coffee_Pot_Control_Protocol
    """
    if flask.request.content_type == "message/coffeepot":
        raise exceptions.IAmATeapotError(
            f"Coffee brewing request for '{flask.request.path}' cannot be completed by teapot application"
        )


def initialize_database() -> None:
    """Initialize the database connection"""
    database.initialize(flask.current_app.appconfig)


class ImageMonkRequest(flask.Request):
    """Extend the default Flask request object to add custom application state settings"""

    def make_response_headers(self) -> ResponseHeaders:
        """Create the headers dictionary of the standard response headers

        This function should be used when determining response headers so that the header names,
        their contents, and formatting are universal.

        :returns: Dictionary of headers
        """

        return {
            constants.HTTP_HEADER_RESPONSE_VERSION: __about__.__version__,
        }


class ImageMonkFlask(flask.Flask):
    """Extend the default Flask object to add the custom application config

    There's probably an easier/more kosher way to do this, but ¯\\_(ツ)_/¯
    """

    request_class = ImageMonkRequest

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appconfig: configuration.ImageMonkConfig = configuration.load()
