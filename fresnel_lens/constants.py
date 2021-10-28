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
    JPEG = ("jpg", "jpeg")
    PNG = ("png",)
    GIF = ("gif",)


class Anchor(enum.Enum):
    C = "center"


HTTP_HEADER_RESPONSE_VERSION = "x-fresnel_lens-version"

HTTP_HEADER_RESPONSE_DIGEST = "Digest"
