from pathlib import Path

from ruamel.yaml import YAML

from dehance.resources._shared import DehanceResource

yaml = YAML(typ="safe")


class OpenAPI(DehanceResource):

    routes = ("/openapi.json",)

    def get(self):

        with (Path(__file__).parent, "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return data, 200
