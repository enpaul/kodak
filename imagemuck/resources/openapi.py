from pathlib import Path

from ruamel.yaml import YAML

from imagemuck.resources._shared import ImageMuckResource

yaml = YAML(typ="safe")


class OpenAPI(ImageMuckResource):

    routes = ("/openapi.json",)

    def get(self):

        with (Path(__file__).parent, "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return data, 200
