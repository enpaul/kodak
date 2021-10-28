from pathlib import Path

from ruamel.yaml import YAML

from fresnel_lens.resources._shared import FresnelResource

yaml = YAML(typ="safe")


class OpenAPI(FresnelResource):

    routes = ("/openapi.json",)

    def get(self):

        with (Path(__file__).parent, "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return data, 200
