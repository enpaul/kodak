import contextlib
import json
from pathlib import Path
from typing import Dict

import pytest

from kodak import configuration
from kodak import constants
from kodak import exceptions


@contextlib.contextmanager
def mockenv(patch, env: Dict[str, str]):
    """Simple context manager for patching in a bunch of env vars"""
    for key, value in env.items():
        patch.setenv(key, value)
    yield
    for key in env:
        patch.delenv(key)


def test_conf_global(monkeypatch):
    """Test the global config object and env parser"""

    assert configuration.KodakConfig() == configuration.load()

    with mockenv(
        monkeypatch,
        {
            "KODAK_SOURCE_DIR": "foobar/baz/",
            "KODAK_CONTENT_DIR": "/var/log/run/proc/sys/class/net/dev/opt/srv",
            "KODAK_EXPOSE_SOURCE": "flalse",
            "KODAK_PRIVATE": "herblegerble",
        },
    ):
        config = configuration.load()
        assert config.source_dir == (Path.cwd() / "foobar" / "baz")
        assert config.content_dir == Path(
            "/", "var", "log", "run", "proc", "sys", "class", "net", "dev", "opt", "srv"
        )
        assert not config.expose_source
        assert not config.private

    with mockenv(
        monkeypatch, {"KODAK_EXPOSE_SOURCE": "false", "KODAK_PRIVATE": "false"}
    ):
        config = configuration.load()
        assert not config.expose_source
        assert not config.private

    with mockenv(monkeypatch, {"KODAK_EXPOSE_SOURCE": "tRuE", "KODAK_PRIVATE": "TruE"}):
        config = configuration.load()
        assert config.expose_source
        assert config.private


def test_conf_database(monkeypatch):
    """Test the database config object and env parser"""

    with mockenv(monkeypatch, {"KODAK_DATABASE_BACKEND": "couchdb"}):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()

    pragmas = {"foo": "bar", "fizz": 1, "buzz": True}
    with mockenv(
        monkeypatch,
        {
            "KODAK_DATABASE_BACKEND": "SQLite",
            "KODAK_DATABASE_SQLITE_PRAGMAS": json.dumps(pragmas),
            "KODAK_DATABASE_SQLITE_PATH": "~/nowhere/nothing.db",
        },
    ):
        config = configuration.load()
        assert config.database.sqlite.pragmas == pragmas
        assert config.database.backend == constants.DatabaseBackend.SQLITE
        assert (
            config.database.sqlite.path
            == Path("~", "nowhere", "nothing.db").expanduser().resolve()
        )
    with mockenv(
        monkeypatch, {"KODAK_DATABASE_SQLITE_PRAGMAS": "this]is{not,valid,,js:on"}
    ):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()

    with mockenv(
        monkeypatch,
        {
            "KODAK_DATABASE_BACKEND": "mariaDB",
        },
    ):
        assert (
            configuration.load().database.backend == constants.DatabaseBackend.MARIADB
        )
    with mockenv(monkeypatch, {"KODAK_DATABASE_MARIADB_PORT": "NaN"}):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()


def test_conf_manip(monkeypatch):
    """Test the manipulation config object and env parser"""

    with mockenv(
        monkeypatch,
        {
            "KODAK_MANIP_BIFF_FORMATS": "png",
            "KODAK_MANIP_BIFF_BLACK_AND_WHITE": "[jonathan frakes voice] its a total fantasy",
        },
    ):
        config = configuration.load()
        assert "biff" in config.manips
        manip = config.manips["biff"]
        assert manip.name == "biff"
        assert manip.formats == {constants.ImageFormat.PNG}
        assert not manip.black_and_white

    with mockenv(
        monkeypatch,
        {
            "KODAK_MANIP_BOFF_NAME": "grand poohbah, de d*ink, of/all%of This&That",
            "KODAK_MANIP_BOFF_FORMATS": "png,jpeg,JPeg",
            "KODAK_MANIP_BOFF_BLACK_AND_WHITE": "truE",
            "KODAK_MANIP_BOFF_CROP_HORIZONTAL": "500",
            "KODAK_MANIP_BOFF_CROP_ANCHOR": "Bottom-Center",
            "KODAK_MANIP_BOFF_SCALE_VERTICAL": "1.5",
            "KODAK_MANIP_BOFF_SCALE_STRATEGY": "RelaTive",
            "KODAK_MANIP_BAFF_CROP_VERTICAL": "128",
            "KODAK_MANIP_BAFF_SCALE_HORIZONTAL": "200",
            "KODAK_MANIP_BAFF_SCALE_STRATEGY": "absoLUTE",
        },
    ):
        config = configuration.load()
        assert "grand poohbah, de d*ink, of/all%of This&That" in config.manips
        assert "baff" in config.manips

        manip = config.manips["grand poohbah, de d*ink, of/all%of This&That"]
        assert manip.name == "grand poohbah, de d*ink, of/all%of This&That"
        assert manip.formats == {constants.ImageFormat.JPEG, constants.ImageFormat.PNG}
        assert manip.black_and_white
        assert manip.crop.horizontal == 500
        assert manip.crop.anchor == constants.CropAnchor.BC
        assert manip.scale.vertical == 1.5
        assert manip.scale.strategy == constants.ScaleStrategy.RELATIVE

        manip = config.manips["baff"]
        assert manip.crop.vertical == 128
        assert manip.scale.horizontal == 200
        assert manip.scale.strategy == constants.ScaleStrategy.ABSOLUTE

    # bad format values
    with mockenv(monkeypatch, {"KODAK_MANIP_TERRIBLE_FORMATS": "jpeg,tiff,woff2"}):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()
    # bad scale strategy value
    with mockenv(
        monkeypatch, {"KODAK_MANIP_TERRIBLE_SCALE_STRATEGY": "take it back now yall"}
    ):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()
    # bad scale value
    with mockenv(
        monkeypatch,
        {
            "KODAK_MANIP_TERRIBLE_SCALE_STRATEGY": "absolute",
            "KODAK_MANIP_TERRIBLE_SCALE_HORIZONTAL": "32.5",
        },
    ):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()
    # bad crop anchor value
    with mockenv(monkeypatch, {"KODAK_MANIP_TERRIBLE_CROP_ANCHOR": "ahoy"}):
        with pytest.raises(exceptions.ConfigurationError):
            configuration.load()
