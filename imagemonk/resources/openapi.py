from pathlib import Path

from ruamel.yaml import YAML

from imagemonk.resources._shared import ImageMonkResource

yaml = YAML(typ="safe")


class OpenAPI(ImageMonkResource):

    routes = ("/openapi.json",)

    def get(self):

        with (Path(__file__).parent, "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return data, 200
