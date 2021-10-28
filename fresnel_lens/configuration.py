import datetime
import enum
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
from typing import Tuple

import peewee

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
class _DBSqliteConfig:
    path: Path = Path.cwd() / "fresnel_lens.db"
    pragmas: Dict[str, Any] = field(default_factory=_default_sqlite_pragmas)

    @classmethod
    def build(cls):
        return cls(
            path=Path(os.environ.get(constants.ENV_CONF_DB_SQLITE_PATH, cls.path)),
            pragmas=json.loads(os.environ[constants.ENV_CONF_DB_SQLITE_PRAGMAS])
            if constants.ENV_CONF_DB_SQLITE_PRAGMAS in os.environ
            else _default_sqlite_pragmas(),
        )


@dataclass
class _DBMariaConfig:

    hostname: str = "localhost"
    username: str = "root"
    password: Optional[str] = None
    port: int = 3306
    schema: str = "fresnel_lens"

    @classmethod
    def build(cls):
        return cls(
            hostname=os.getenv(constants.ENV_CONF_DB_MARIA_HOSTNAME, cls.hostname),
            username=os.getenv(constants.ENV_CONF_DB_MARIA_USERNAME, cls.username),
            password=os.environ.get(constants.ENV_CONF_DB_MARIA_PASSWORD, cls.password),
            port=int(os.environ.get(constants.ENV_CONF_DB_MARIA_PORT, cls.port)),
            schema=os.getenv(constants.ENV_CONF_DB_MARIA_SCHEMA, cls.schema),
        )


@dataclass
class _DBConfig:

    backend: constants.DatabaseBackend = constants.DatabaseBackend.SQLITE
    sqlite: _DBSqliteConfig = field(default_factory=_DBSqliteConfig.build)
    mariadb: _DBMariaConfig = field(default_factory=_DBMariaConfig.build)

    @classmethod
    def build(cls):
        return cls(
            backend=constants.DatabaseBackend[os.environ[constants.ENV_CONF_DB_BACKEND]]
            if constants.ENV_CONF_DB_BACKEND in os.environ
            else cls.backend
        )


@dataclass
class ManipConfig:
    alias: str
    formats: Sequence[constants.ImageFormat] = (
        constants.ImageFormat.JPEG,
        constants.ImageFormat.PNG,
    )
    horizontal: None
    vertical: None


@dataclass
class ImageMuckConfig:
    database: _DBConfig = field(default_factory=_DBConfig.build)
    images: Path = Path.cwd() / "images"
    cache_dir: Path = Path.cwd() / "cache"
    expose_source: bool = False
    manips: Sequence[ManipConfig] = ()

    @classmethod
    def from_env(cls):
        return cls(
            storage_path=Path(
                os.getenv(constants.ENV_CONF_FS_STORAGE_PATH, cls.storage_path)
            ).resolve()
        )


def load() -> ImageMuckConfig:
    return ImageMuckConfig.from_env()
