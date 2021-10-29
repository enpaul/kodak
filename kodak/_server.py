import flask

from kodak import configuration
from kodak import database
from kodak import exceptions


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


class KodakFlask(flask.Flask):
    """Extend the default Flask object to add the custom application config

    There's probably an easier/more kosher way to do this, but ¯\\_(ツ)_/¯
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appconfig: configuration.KodakConfig = configuration.load()
