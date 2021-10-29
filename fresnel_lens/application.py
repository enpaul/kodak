import flask_restful

from fresnel_lens import resources
from fresnel_lens._server import FresnelFlask
from fresnel_lens._server import initialize_database
from fresnel_lens._server import make_the_tea


APPLICATION = FresnelFlask(__name__)
API = flask_restful.Api(APPLICATION, catch_all_404s=True)


APPLICATION.before_request(make_the_tea)
APPLICATION.before_first_request(initialize_database)

for resource in resources.RESOURCES:
    API.add_resource(resource, *resource.routes)
