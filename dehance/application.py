import flask_restful

from dehance import resources
from dehance._server import DehanceFlask
from dehance._server import initialize_database
from dehance._server import make_the_tea


APPLICATION = DehanceFlask(__name__)
API = flask_restful.Api(APPLICATION, catch_all_404s=True)


def _set_upload_limit() -> None:
    APPLICATION.config["MAX_CONTENT_LENGTH"] = APPLICATION.appconfig.upload.size_limit


APPLICATION.before_request(make_the_tea)
APPLICATION.before_first_request(initialize_database)
APPLICATION.before_first_request(_set_upload_limit)

for resource in resources.RESOURCES:
    API.add_resource(resource, *resource.routes)
