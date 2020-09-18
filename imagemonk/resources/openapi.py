from pathlib import Path

import flask_restful
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class OpenAPI(flask_restful.Resource):
    def get(self):

        with (Path(__file__).parent, "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return data, 200
