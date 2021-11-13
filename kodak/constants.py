import enum
from typing import Any
from typing import Dict
from typing import Set

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

    JPEG = ("jpg", "jpeg")
    PNG = ("png",)


DEFAULT_SQLITE_PRAGMAS: Dict[str, Any] = {
    "journal_mode": "wal",
    "cache_size": -1 * 64000,
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
    "synchronous": 0,
}

SQLITE_VARIABLE_LIMIT = 999

DEFAULT_SUPPORTED_FORMATS: Set[ImageFormat] = {ImageFormat.JPEG, ImageFormat.PNG}

IMAGE_PATH_NAME_SEPARATOR: str = "-"

IMAGE_FILE_EXTENSIONS: Set[str] = set()

for item in ImageFormat:
    for ext in item.value:
        IMAGE_FILE_EXTENSIONS.add(f".{ext}")
