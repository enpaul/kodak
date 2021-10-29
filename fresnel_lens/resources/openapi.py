from pathlib import Path

from ruamel.yaml import YAML

from fresnel_lens.resources._shared import FresnelResource
from fresnel_lens.resources._shared import ResponseTuple

yaml = YAML(typ="safe")


class OpenAPI(FresnelResource):
    """Handle requests for the OpenAPI specification resource"""

    routes = ("/openapi.json",)

    def get(self) -> ResponseTuple:
        """Retrieve the OpenAPI specification document"""
        with (Path(__file__).parent / "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return self.make_response(data)

    def head(self) -> ResponseTuple:
        """Alias of GET with no response body"""
        return self._head(self.get())
