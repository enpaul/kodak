import importlib.resources

import openapi_spec_validator
import ruamel.yaml

from kodak import __about__


yaml = ruamel.yaml.YAML(typ="safe")  # pylint: disable=invalid-name


def test_openapi():
    openapi_spec_validator.validate_spec(
        yaml.load(importlib.resources.read_text("kodak", "openapi.yaml"))
    )


def test_openapi_version():
    spec = yaml.load(importlib.resources.read_text("kodak", "openapi.yaml"))
    assert spec["info"]["version"] == __about__.__version__
