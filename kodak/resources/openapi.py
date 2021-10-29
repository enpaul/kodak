from pathlib import Path

from ruamel.yaml import YAML

from kodak.resources._shared import KodakResource
from kodak.resources._shared import ResponseTuple

yaml = YAML(typ="safe")


class OpenAPI(KodakResource):
    """Handle requests for the OpenAPI specification resource"""

    routes = ("/openapi.json",)

    def get(self) -> ResponseTuple:
        """Retrieve the OpenAPI specification document"""
        with (Path(__file__).parent / "openapi.yaml").open() as infile:
            data = yaml.load(infile)

        return self.make_response(data)

    def head(self) -> ResponseTuple:
        """Alias HEAD to GET"""
        return self._head(self.get())
