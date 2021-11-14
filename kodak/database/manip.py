import peewee

from kodak import constants
from kodak.database._shared import ChecksumField
from kodak.database._shared import EnumField
from kodak.database._shared import KodakModel
from kodak.database._shared import PathField
from kodak.database.image import ImageRecord


class ManipRecord(KodakModel):
    """Model for manipulated image records"""

    parent = peewee.ForeignKeyField(ImageRecord, null=False)
    manip = peewee.CharField(null=False)
    file = PathField(null=False)
    format_ = EnumField(constants.ImageFormat, null=False)
    checksum = ChecksumField(null=False)
