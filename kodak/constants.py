import enum

import peewee


class DatabaseBackend(enum.Enum):
    """Enum of supported database backends"""

    MARIADB = peewee.MySQLDatabase
    SQLITE = peewee.SqliteDatabase


class ScaleStrategy(enum.Enum):
    """Available strategies for scaling images"""

    RELATIVE = enum.auto()
    ABSOLUTE = enum.auto()


class CropAnchor(enum.Enum):
    """Anchor locations for cropping images"""

    TL = "top-left"
    TC = "top-center"
    TR = "top-center"
    CL = "center-left"
    C = "center"
    CR = "center-right"
    BL = "bottom-left"
    BC = "bottom-center"
    BR = "bottom-right"


class ImageFormat(enum.Enum):
    """Supported image conversion formats"""

    JPEG = enum.auto()
    PNG = enum.auto()


DEFAULT_SQLITE_PRAGMAS = {
    "journal_mode": "wal",
    "cache_size": -1 * 64000,
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
    "synchronous": 0,
}

DEFAULT_SUPPORTED_FORMATS = {ImageFormat.JPEG, ImageFormat.PNG}
