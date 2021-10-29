"""Test that metadata module matches pyproject"""
from pathlib import Path

import toml

from kodak import __about__


def test_about():
    """Test metadata values"""

    with (Path(__file__).resolve().parent.parent / "pyproject.toml").open() as infile:
        pyproject = toml.load(infile)

    assert pyproject["tool"]["poetry"]["name"] == __about__.__title__
    assert pyproject["tool"]["poetry"]["version"] == __about__.__version__
    assert pyproject["tool"]["poetry"]["license"] == __about__.__license__
    assert pyproject["tool"]["poetry"]["description"] == __about__.__summary__
    assert pyproject["tool"]["poetry"]["repository"] == __about__.__url__
    assert (
        all(
            item in __about__.__authors__
            for item in pyproject["tool"]["poetry"]["authors"]
        )
        is True
    )
    assert (
        all(
            item in pyproject["tool"]["poetry"]["authors"]
            for item in __about__.__authors__
        )
        is True
    )
