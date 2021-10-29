import enum

import peewee


class DatabaseBackend(enum.Enum):
    MARIADB = peewee.MySQLDatabase
    SQLITE = peewee.SqliteDatabase


class DimensionStrategy(enum.Enum):
    CROP = enum.auto()
    SCALE = enum.auto()
    RELATIVE = enum.auto()


class ImageFormat(enum.Enum):
    JPEG = enum.auto()
    PNG = enum.auto()
    GIF = enum.auto()


class Anchor(enum.Enum):
    TL = "top-left"
    TC = "top-center"
    TR = "top-center"
    CL = "center-left"
    C = "center"
    CR = "center-right"
    BL = "bottom-left"
    BC = "bottom-center"
    BR = "bottom-right"


DEFAULT_SQLITE_PRAGMAS = {
    "journal_mode": "wal",
    "cache_size": -1 * 64000,
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
    "synchronous": 0,
}
