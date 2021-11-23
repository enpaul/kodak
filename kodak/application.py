import flask_restful

from kodak import index
from kodak import resources
from kodak._server import initialize_database
from kodak._server import KodakFlask
from kodak._server import make_the_tea


APPLICATION = KodakFlask(__name__)
API = flask_restful.Api(APPLICATION, catch_all_404s=True)


APPLICATION.before_request(make_the_tea)
APPLICATION.before_first_request(initialize_database)
APPLICATION.before_first_request(index.build)

for resource in resources.RESOURCES:
    API.add_resource(resource, *resource.routes)
