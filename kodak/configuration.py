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
from typing import Type
from typing import Union

from kodak import constants
from kodak import exceptions


def _get_int(var: str, default: Optional[int]) -> Optional[int]:
    return int(os.environ[var]) if var in os.environ else default


def _get_float(var: str, default: Optional[float]) -> Optional[float]:
    return float(os.environ[var]) if var in os.environ else default


def _get_enum_by_name(
    var: str, enumeration: Type[enum.Enum], default: enum.Enum
) -> enum.Enum:
    return enumeration[os.environ[var].upper()] if var in os.environ else default


def _get_enum_by_value(
    var: str, enumeration: Type[enum.Enum], default: enum.Enum
) -> enum.Enum:
    return enumeration(os.environ[var].lower()) if var in os.environ else default


def _get_path(var: str, default: Union[str, Path]) -> Path:
    return Path(os.environ.get(var, default)).expanduser().resolve()


def _get_bool(var: str, default: bool) -> bool:
    return os.getenv(var, str(default)).lower() == "true"


@dataclass
class DatabaseSqliteConfig:
    """SQLite database backend configuration options

    :param path: Path to the SQLite database file
    :param pragmas: Mapping of SQLite pragmas to apply to the database connection
    """

    path: Path = Path.cwd() / "kodak.db"
    pragmas: Dict[str, Any] = field(
        default_factory=lambda: constants.DEFAULT_SQLITE_PRAGMAS
    )

    @classmethod
    def from_env(cls):
        """Build dataclass from environment"""
        return cls(
            path=_get_path("KODAK_DATABASE_SQLITE_PATH", cls.path),
            pragmas=json.loads(os.environ["KODAK_DATABASE_SQLITE_PRAGMAS"])
            if "KODAK_DATABASE_SQLITE_PRAGMAS" in os.environ
            else constants.DEFAULT_SQLITE_PRAGMAS,
        )


@dataclass
class DatabaseMariaConfig:
    """MariaDB database backend configuration options

    :param hostname: Hostname or IP address of the host running the database server
    :param username: Username of the account to use for connecting to the database server
    :param password: Password for the account to use for connecting to the database server
    :param port: Port on the host that the database server is listening on
    :param schema: Database schema that the application should use
    """

    hostname: str = "localhost"
    username: str = "root"
    password: Optional[str] = None
    port: int = 3306
    schema: str = "kodak"

    @classmethod
    def from_env(cls):
        """Build dataclass from environment"""
        return cls(
            hostname=os.getenv("KODAK_DATABASE_MARIADB_HOSTNAME", cls.hostname),
            username=os.getenv("KODAK_DATABASE_MARIADB_USERNAME", cls.username),
            password=os.environ.get("KODAK_DATABASE_MARIADB_PASSWORD", cls.password),
            port=_get_int("KODAK_DATABASE_MARIADB_PORT", cls.port),
            schema=os.getenv("KODAK_DATABASE_MARIADB_SCHEMA", cls.schema),
        )


@dataclass
class DatabaseConfig:
    """Database backend configuration

    :param backend: Enum selecting the backend to use for storing data
    :param sqlite: Container of SQLite settings
    :param mariadb: Container of MariaDB settings
    """

    backend: constants.DatabaseBackend = constants.DatabaseBackend.SQLITE
    sqlite: DatabaseSqliteConfig = field(default_factory=DatabaseSqliteConfig.from_env)
    mariadb: DatabaseMariaConfig = field(default_factory=DatabaseMariaConfig.from_env)

    @classmethod
    def from_env(cls):
        """Build dataclass from environment"""
        return cls(
            backend=_get_enum_by_name(
                "KODAK_DATABASE_BACKEND", constants.DatabaseBackend, cls.backend
            )
        )


@dataclass
class ManipCropConfig:
    """Settings for cropping an image

    :param horizontal: Size the image should be cropped to (in pixels) in the horizontal direction
    :param vertical: Size the image should be cropped to (in pixels) in the vertical direction
    :param anchor: Image location anchor that cropping should be done relative to
    """

    horizontal: Optional[int] = None
    vertical: Optional[int] = None
    anchor: constants.CropAnchor = constants.CropAnchor.C

    @classmethod
    def from_env(cls, key: str):
        """Build dataclass from environment"""
        return cls(
            anchor=_get_enum_by_value(  # type: ignore
                f"KODAK_MANIP_{key}_CROP_ANCHOR", constants.CropAnchor, cls.anchor
            ),
            horizontal=_get_int(f"KODAK_MANIP_{key}_CROP_HORIZONTAL", cls.horizontal),
            vertical=_get_int(f"KODAK_MANIP_{key}_CROP_VERTICAL", cls.vertical),
        )


@dataclass
class ManipScaleConfig:
    """Settings for scaling an image

    :param horizontal: Horizontal scaling dimension. If ``strategy`` is ``ABSOLUTE`` then this is
                       the pixel measurement that the horizontal dimension will be scaled up or
                       down to; if ``strategy`` is ``RELATIVE`` then this is a percentage modifier
                       that will be applied to the image's existing horizontal dimension.
    :param vertical: Vertical scaling dimension. If ``strategy`` is ``ABSOLUTE`` then this is the
                     pixel measurement that the vertical dimension will be scaled up or down to;
                     if ``strategy`` is ``RELATIVE`` then this is a percentage modifier that will
                     be applied to the image's existing vertical dimension.
    :param strategy: Strategy to use for scaling the image. Use ``ABSOLUTE`` to scale to an
                     absolute pixel measurement and use ``RELATIVE`` to scale relative to the
                     existing dimensions.
    """

    horizontal: Optional[Union[int, float]] = None
    vertical: Optional[Union[int, float]] = None
    strategy: constants.ScaleStrategy = constants.ScaleStrategy.ABSOLUTE

    @classmethod
    def from_env(cls, key: str):
        """Build dataclass from environment"""
        strategy = _get_enum_by_name(
            f"KODAK_MANIP_{key}_SCALE_STRATEGY", constants.ScaleStrategy, cls.strategy
        )

        if strategy == constants.ScaleStrategy.ABSOLUTE:
            parser = _get_int  # type: ignore
        elif strategy == constants.ScaleStrategy.RELATIVE:
            parser = _get_float  # type: ignore
        else:
            raise RuntimeError("This path should not be possible")

        return cls(
            strategy=strategy,  # type: ignore
            vertical=parser(f"KODAK_MANIP_{key}_SCALE_VERTICAL", cls.vertical),  # type: ignore
            horizontal=parser(f"KODAK_MANIP_{key}_SCALE_HORIZONTAL", cls.horizontal),  # type: ignore
        )


@dataclass
class ManipConfig:
    """Image manipulation configuration settings

    :param name: Name of the manipulation that will be accessed in the URL
    :param crop: Contaienr of settings for cropping an image
    :param scale: Container of settings for scaling an image
    :param formats: Set of image formats that the source can be dynamically converted into
    :param black_and_white: Whether the image should be converted to black and white
    """

    name: str
    crop: ManipCropConfig = field(default_factory=ManipCropConfig)
    scale: ManipScaleConfig = field(default_factory=ManipScaleConfig)
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
        """Build dataclass from environment"""
        name = os.getenv(f"KODAK_MANIP_{key}_NAME", key.lower())

        if name == "original":
            raise exceptions.ConfigurationError(
                "Manipulation name 'original' is reserved for application usage"
            )

        return cls(
            name=name,
            crop=ManipCropConfig.from_env(key),
            scale=ManipScaleConfig.from_env(key),
            formats=set(
                constants.ImageFormat[item.strip().upper()]
                for item in os.environ[f"KODAK_MANIP_{key}_FORMATS"].split(",")
            )
            if f"KODAK_MANIP_{key}_FORMATS" in os.environ
            else constants.DEFAULT_SUPPORTED_FORMATS,
            black_and_white=_get_bool(
                f"KODAK_MANIP_{key}_BLACK_AND_WHITE", cls.black_and_white
            ),
        )


@dataclass
class KodakConfig:
    """Global application configuration settings

    :param database: Container of database backend settings
    :param manips: Mapping of manipulation config names to image manipulation configurations
    :param source_dir: Path to where source images should be loaded from
    :param content_dir: Path to where the application should store generated images
    :param expose_source: Whether the original image should be exposed to clients
    :param private: Whether authentication is required for accessing the server
    """

    database: DatabaseConfig = field(default_factory=DatabaseConfig.from_env)
    manips: Dict[str, ManipConfig] = field(default_factory=dict)
    source_dir: Path = Path.cwd() / "pictures"
    content_dir: Path = Path.cwd() / "content"
    expose_source: bool = False
    private: bool = False

    @classmethod
    def from_env(cls):
        """Build dataclass from environment"""
        manip_names = set(
            key.replace("KODAK_MANIP_", "").partition("_")[0]
            for key in os.environ
            if key.startswith("KODAK_MANIP_")
        )
        manips = [ManipConfig.from_env(name) for name in manip_names]
        return cls(
            source_dir=_get_path("KODAK_SOURCE_DIR", cls.source_dir),
            content_dir=_get_path("KODAK_CONTENT_DIR", cls.content_dir),
            expose_source=_get_bool("KODAK_EXPOSE_SOURCE", cls.expose_source),
            private=_get_bool("KODAK_PRIVATE", cls.private),
            manips={item.name: item for item in manips},
        )


def load() -> KodakConfig:
    """Load the application configuration from environment variables

    :returns: Populated environment configuration
    """
    try:
        return KodakConfig.from_env()
    except (ValueError, TypeError, IndexError, KeyError) as err:
        raise exceptions.ConfigurationError(f"Failed to load configuration: {err}")
