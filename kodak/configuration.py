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

from kodak import constants


class DimensionConfig(NamedTuple):
    strategy: constants.DimensionStrategy
    anchor: constants.Anchor
    value: int


@dataclass
class DatabaseSqliteConfig:
    path: Path = Path.cwd() / "fresnel.db"
    pragmas: Dict[str, Any] = field(
        default_factory=lambda: constants.DEFAULT_SQLITE_PRAGMAS
    )

    @classmethod
    def from_env(cls):
        return cls(
            path=Path(os.environ.get("KODAK_DB_SQLITE_PATH", cls.path)),
            pragmas=json.loads(os.environ["KODAK_DB_SQLITE_PRAGMAS"])
            if "KODAK_DB_SQLITE_PRAGMAS" in os.environ
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
            hostname=os.getenv("KODAK_DB_MARIA_HOSTNAME", cls.hostname),
            username=os.getenv("KODAK_DB_MARIA_USERNAME", cls.username),
            password=os.environ.get("KODAK_DB_MARIA_PASSWORD", cls.password),
            port=int(os.environ.get("KODAK_DB_MARIA_PORT", cls.port)),
            schema=os.getenv("KODAK_DB_MARIA_SCHEMA", cls.schema),
        )


@dataclass
class DatabaseConfig:

    backend: constants.DatabaseBackend = constants.DatabaseBackend.SQLITE
    sqlite: DatabaseSqliteConfig = field(default_factory=DatabaseSqliteConfig.from_env)
    mariadb: DatabaseMariaConfig = field(default_factory=DatabaseMariaConfig.from_env)

    @classmethod
    def from_env(cls):
        return cls(
            backend=constants.DatabaseBackend[os.environ["KODAK_DB_BACKEND"].upper()]
            if "KODAK_DB_BACKEND" in os.environ
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
                os.environ[f"KODAK_MANIP_{key}_STRATEGY"].upper()
            ]
            if f"KODAK_MANIP_{key}_STRATEGY" in os.environ
            else cls.strategy
        )

        dimension_conversion = (
            float if strategy == constants.DimensionStrategy.RELATIVE else int
        )

        return cls(
            name=os.getenv(f"KODAK_MANIP_{key}_NAME", key.lower()),
            strategy=strategy,
            anchor=constants.Anchor(os.environ[f"KODAK_MANIP_{key}_ANCHOR"].lower())
            if f"KODAK_MANIP_{key}_ANCHOR" in os.environ
            else cls.anchor,
            formats=[
                constants.ImageFormat[item.upper()]
                for item in os.environ[f"KODAK_MANIP_{key}_FORMATS"].split(",")
            ]
            if f"KODAK_MANIP_{key}_FORMATS" in os.environ
            else cls.formats,
            horizontal=dimension_conversion(os.environ[f"KODAK_MANIP_{key}_HORIZONTAL"])
            if f"KODAK_MANIP_{key}_HORIZONTAL" in os.environ
            else cls.horizontal,
            vertical=dimension_conversion(os.environ[f"KODAK_MANIP_{key}_VERTICAL"])
            if f"KODAK_MANIP_{key}_VERTICAL" in os.environ
            else cls.vertical,
        )


@dataclass
class KodakConfig:
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
                key.replace("KODAK_MANIP_", "").partition("_")[0]
                for key in os.environ.keys()
                if key.startswith("KODAK_MANIP_")
            ]
        )
        return cls(
            sourcedir=Path(os.environ.get("KODAK_SOURCEDIR", cls.sourcedir))
            .expanduser()
            .resolve(),
            manipdir=Path(os.environ.get("KODAK_MANIPDIR", cls.manipdir))
            .expanduser()
            .resolve(),
            expose_source=os.getenv(
                "KODAK_EXPOSE_SOURCE", str(cls.expose_source)
            ).lower()
            == "true",
            private=os.getenv("KODAK_PRIVATE", str(cls.private)).lower() == "true",
            manips={name.lower(): ManipConfig.from_env(name) for name in manip_names},
        )


def load() -> KodakConfig:
    try:
        return KodakConfig.from_env()
    except (ValueError, TypeError, IndexError, KeyError) as err:
        raise RuntimeError(err)
