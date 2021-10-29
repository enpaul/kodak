import json
import os
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Union

from fresnel_lens import constants


class DimensionConfig(NamedTuple):
    strategy: constants.DimensionStrategy
    anchor: constants.Anchor
    value: int


def _default_sqlite_pragmas() -> Dict[str, Any]:
    """Default SQLite pragmas

    .. note:: This needs to be a separate callout function to avoid setting a mutable type in the
              dataclass signature.

    .. note:: These settings are taken directly from
              `the Peewee docs <http://docs.peewee-orm.com/en/latest/peewee/database.html#recommended-settings>`_.
    """
    return {
        "journal_mode": "wal",
        "cache_size": -1 * 64000,
        "foreign_keys": 1,
        "ignore_check_constraints": 0,
        "synchronous": 0,
    }


@dataclass
class DatabaseSqliteConfig:
    path: Path = Path.cwd() / "fresnel.db"
    pragmas: Dict[str, Any] = field(default_factory=_default_sqlite_pragmas)

    @classmethod
    def from_env(cls):
        return cls(
            path=Path(os.environ.get("FRESNEL_DB_SQLITE_PATH", cls.path)),
            pragmas=json.loads(os.environ["FRESNEL_DB_SQLITE_PRAGMAS"])
            if "FRESNEL_DB_SQLITE_PRAGMAS" in os.environ
            else constants.DEFAULT_SQLITE_PRAGMAS,
        )


@dataclass
class DatabaseMariaConfig:

    hostname: str = "localhost"
    username: str = "root"
    password: Optional[str] = None
    port: int = 3306
    schema: str = "fresnel"

    @classmethod
    def from_env(cls):
        return cls(
            hostname=os.getenv("FRESNEL_DB_MARIA_HOSTNAME", cls.hostname),
            username=os.getenv("FRESNEL_DB_MARIA_USERNAME", cls.username),
            password=os.environ.get("FRESNEL_DB_MARIA_PASSWORD", cls.password),
            port=int(os.environ.get("FRESNEL_DB_MARIA_PORT", cls.port)),
            schema=os.getenv("FRESNEL_DB_MARIA_SCHEMA", cls.schema),
        )


@dataclass
class DatabaseConfig:

    backend: constants.DatabaseBackend = constants.DatabaseBackend.SQLITE
    sqlite: DatabaseSqliteConfig = field(default_factory=DatabaseSqliteConfig.from_env)
    mariadb: DatabaseMariaConfig = field(default_factory=DatabaseMariaConfig.from_env)

    @classmethod
    def from_env(cls):
        return cls(
            backend=constants.DatabaseBackend[os.environ["FRESNEL_DB_BACKEND"].upper()]
            if "FRESNEL_DB_BACKEND" in os.environ
            else cls.backend
        )


@dataclass
class ManipConfig:
    name: str
    strategy: constants.DimensionStrategy = constants.DimensionStrategy.SCALE
    anchor: constants.Anchor = constants.Anchor.C
    formats: Sequence[constants.ImageFormat] = (
        constants.ImageFormat.JPEG,
        constants.ImageFormat.PNG,
    )
    horizontal: Optional[Union[int, float]] = None
    vertical: Optional[Union[int, float]] = None

    @classmethod
    def from_env(cls, key: str):
        strategy = (
            constants.DimensionStrategy[
                os.environ[f"FRESNEL_MANIP_{key}_STRATEGY"].upper()
            ]
            if f"FRESNEL_MANIP_{key}_STRATEGY" in os.environ
            else cls.strategy
        )

        dimension_conversion = (
            float if strategy == constants.DimensionStrategy.RELATIVE else int
        )

        return cls(
            name=os.getenv(f"FRESNEL_MANIP_{key}_NAME", key.lower()),
            strategy=strategy,
            anchor=constants.Anchor(os.environ[f"FRESNEL_MANIP_{key}_ANCHOR"].lower())
            if f"FRESNEL_MANIP_{key}_ANCHOR" in os.environ
            else cls.anchor,
            formats=[
                constants.ImageFormat[item.upper()]
                for item in os.environ[f"FRESNEL_MANIP_{key}_FORMATS"].split(",")
            ]
            if f"FRESNEL_MANIP_{key}_FORMATS" in os.environ
            else cls.formats,
            horizontal=dimension_conversion(
                os.environ[f"FRESNEL_MANIP_{key}_HORIZONTAL"]
            )
            if f"FRESNEL_MANIP_{key}_HORIZONTAL" in os.environ
            else cls.horizontal,
            vertical=dimension_conversion(os.environ[f"FRESNEL_MANIP_{key}_VERTICAL"])
            if f"FRESNEL_MANIP_{key}_VERTICAL" in os.environ
            else cls.vertical,
        )


@dataclass
class FresnelConfig:
    database: DatabaseConfig = field(default_factory=DatabaseConfig.from_env)
    sourcedir: Path = Path.cwd() / "images"
    manipdir: Path = Path.cwd() / "images"
    expose_source: bool = False
    private: bool = False
    manips: Dict[str, ManipConfig] = field(default_factory=dict)

    @classmethod
    def from_env(cls):
        manip_names = set(
            [
                key.replace("FRESNEL_MANIP_", "").partition("_")[0]
                for key in os.environ.keys()
                if key.startswith("FRESNEL_MANIP_")
            ]
        )
        return cls(
            sourcedir=Path(os.environ.get("FRESNEL_SOURCEDIR", cls.sourcedir))
            .expanduser()
            .resolve(),
            manipdir=Path(os.environ.get("FRESNEL_MANIPDIR", cls.manipdir))
            .expanduser()
            .resolve(),
            expose_source=os.getenv(
                "FRESNEL_EXPOSE_SOURCE", str(cls.expose_source)
            ).lower()
            == "true",
            private=os.getenv("FRESNEL_PRIVATE", str(cls.private)).lower() == "true",
            manips={name.lower(): ManipConfig.from_env(name) for name in manip_names},
        )


def load() -> FresnelConfig:
    try:
        return FresnelConfig.from_env()
    except (ValueError, TypeError, IndexError, KeyError) as err:
        raise RuntimeError(err)
