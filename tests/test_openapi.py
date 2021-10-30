import importlib.resources

import openapi_spec_validator
import ruamel.yaml

from kodak import __about__


yaml = ruamel.yaml.YAML(typ="safe")  # pylint: disable=invalid-name


def test_openapi():
    """Validate the OpenAPI specification document structure"""
    openapi_spec_validator.validate_spec(
        yaml.load(importlib.resources.read_text("kodak", "openapi.yaml"))
    )


def test_openapi_version():
    """Check that the OpenAPI metadata matches the package metadata"""
    spec = yaml.load(importlib.resources.read_text("kodak", "openapi.yaml"))
    assert spec["info"]["version"] == __about__.__version__
    assert spec["info"]["license"]["name"] == __about__.__license__
    assert spec["info"]["title"].lower() == __about__.__title__.lower()
