"""Test that metadata module matches pyproject"""
from pathlib import Path

import toml

from imagemonk import __about__


def test_about():
    """Test metadata values"""

    with (Path(__file__).parent.parent / "pyproject.toml").open() as infile:
        about = toml.load(infile)

    assert about["tool"]["poetry"]["name"] == __about__.__title__
    assert about["tool"]["poetry"]["version"] == __about__.__version__
    assert all(
        author in about["tool"]["poetry"]["authors"] for author in __about__.__authors__
    )
    assert all(
        author in __about__.__authors__ for author in about["tool"]["poetry"]["authors"]
    )
