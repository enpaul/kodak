import enum
import json
import os
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional
from typing import Set
from typing import Union

from kodak import constants
from kodak import exceptions


def _get_int(var: str, default: Optional[int]) -> Optional[int]:
    return int(os.environ[var]) if var in os.environ else default


def _get_float(var: str, default: Optional[float]) -> Optional[float]:
    return float(os.environ[var]) if var in os.environ else default


def _get_enum_by_name(
    var: str, enumeration: enum.Enum, default: enum.Enum
) -> enum.Enum:
    return enumeration[os.environ[var].upper()] if var in os.environ else default


def _get_enum_by_value(
    var: str, enumeration: enum.Enum, default: enum.Enum
) -> enum.Enum:
    return enumeration(os.environ[var].lower()) if var in os.environ else default


def _get_path(var: str, default: Union[str, Path]) -> Path:
    return Path(os.environ.get(var, default)).expanduser().resolve()


def _get_bool(var: str, default: bool) -> bool:
    return os.getenv(var, str(default)).lower() == "true"


@dataclass
class DatabaseSqliteConfig:
    path: Path = Path.cwd() / "fresnel.db"
    pragmas: Dict[str, Any] = field(
        default_factory=lambda: constants.DEFAULT_SQLITE_PRAGMAS
    )

    @classmethod
    def from_env(cls):
        return cls(
            path=_get_path("KODAK_DATABASE_SQLITE_PATH", cls.path),
            pragmas=json.loads(os.environ["KODAK_DATABASE_SQLITE_PRAGMAS"])
            if "KODAK_DATABASE_SQLITE_PRAGMAS" in os.environ
            else constants.DEFAULT_SQLITE_PRAGMAS,
        )


@dataclass
class DatabaseMariaConfig:

    hostname: str = "localhost"
    username: str = "root"
    password: Optional[str] = None
    port: int = 3306
    schema: str = "kodak"

    @classmethod
    def from_env(cls):
        return cls(
            hostname=os.getenv("KODAK_DATABASE_MARIADB_HOSTNAME", cls.hostname),
            username=os.getenv("KODAK_DATABASE_MARIADB_USERNAME", cls.username),
            password=os.environ.get("KODAK_DATABASE_MARIADB_PASSWORD", cls.password),
            port=_get_int("KODAK_DATABASE_MARIADB_PORT", cls.port),
            schema=os.getenv("KODAK_DATABASE_MARIADB_SCHEMA", cls.schema),
        )


@dataclass
class DatabaseConfig:

    backend: constants.DatabaseBackend = constants.DatabaseBackend.SQLITE
    sqlite: DatabaseSqliteConfig = field(default_factory=DatabaseSqliteConfig.from_env)
    mariadb: DatabaseMariaConfig = field(default_factory=DatabaseMariaConfig.from_env)

    @classmethod
    def from_env(cls):
        return cls(
            backend=_get_enum_by_name(
                "KODAK_DATABASE_BACKEND", constants.DatabaseBackend, cls.backend
            )
        )


@dataclass
class ManipCropConfig:
    horizontal: Optional[int] = None
    vertical: Optional[int] = None
    anchor: constants.CropAnchor = constants.CropAnchor.C

    @classmethod
    def from_env(cls, key: str):
        return cls(
            anchor=_get_enum_by_value(
                f"KODAK_MANIP_{key}_CROP_ANCHOR", constants.CropAnchor, cls.anchor
            ),
            horizontal=_get_int(f"KODAK_MANIP_{key}_CROP_HORIZONTAL", cls.horizontal),
            vertical=_get_int(f"KODAK_MANIP_{key}_CROP_VERTICAL", cls.vertical),
        )


@dataclass
class ManipScaleConfig:
    horizontal: Optional[Union[int, float]] = None
    vertical: Optional[Union[int, float]] = None
    strategy: constants.ScaleStrategy = constants.ScaleStrategy.ABSOLUTE

    @classmethod
    def from_env(cls, key: str):
        strategy = _get_enum_by_name(
            f"KODAK_MANIP_{key}_SCALE_STRATEGY", constants.ScaleStrategy, cls.strategy
        )

        if strategy == constants.ScaleStrategy.ABSOLUTE:
            parser = _get_int
        elif strategy == constants.ScaleStrategy.RELATIVE:
            parser = _get_float
        else:
            raise RuntimeError("This path should not be possible")

        return cls(
            strategy=strategy,
            vertical=parser(f"KODAK_MANIP_{key}_SCALE_VERTICAL", cls.vertical),
            horizontal=parser(f"KODAK_MANIP_{key}_SCALE_HORIZONTAL", cls.horizontal),
        )


@dataclass
class ManipConfig:
    name: str
    crop: ManipCropConfig = field(default_factory=ManipCropConfig.from_env)
    scale: ManipScaleConfig = field(default_factory=ManipScaleConfig.from_env)
    formats: Set[constants.ImageFormat] = field(
        default_factory=lambda: constants.DEFAULT_SUPPORTED_FORMATS
    )
    black_and_white: bool = False
    # TODO: Implement support for these settings
    # brightness: int = 0
    # contrast: int = 0
    # sepia: bool = False

    @classmethod
    def from_env(cls, key: str):
        return cls(
            name=os.getenv(f"KODAK_MANIP_{key}_NAME", key.lower()),
            crop=ManipCropConfig.from_env(key),
            scale=ManipScaleConfig.from_env(key),
            formats=set(
                [
                    constants.ImageFormat[item.strip().upper()]
                    for item in os.environ[f"KODAK_MANIP_{key}_FORMATS"].split(",")
                ]
            )
            if f"KODAK_MANIP_{key}_FORMATS" in os.environ
            else constants.DEFAULT_SUPPORTED_FORMATS,
            black_and_white=_get_bool(
                f"KODAK_MANIP_{key}_BLACK_AND_WHITE", cls.black_and_white
            ),
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
            sourcedir=_get_path("KODAK_SOURCEDIR", cls.sourcedir),
            manipdir=_get_path("KODAK_MANIPDIR", cls.manipdir),
            expose_source=_get_bool("KODAK_EXPOSE_SOURCE", cls.expose_source),
            private=_get_bool("KODAK_PRIVATE", cls.private),
            manips={name.lower(): ManipConfig.from_env(name) for name in manip_names},
        )


def load() -> KodakConfig:
    try:
        return KodakConfig.from_env()
    except (ValueError, TypeError, IndexError, KeyError) as err:
        raise exceptions.ConfigurationError(f"Failed to load configuration: {err}")
