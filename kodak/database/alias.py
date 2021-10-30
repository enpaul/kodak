import peewee

from kodak.database._shared import ChecksumField
from kodak.database._shared import KodakModel
from kodak.database.image import ImageRecord


class AliasRecord(KodakModel):
    """Model for manipulated image records"""

    parent = peewee.ForeignKeyField(ImageRecord, null=False)
    name = peewee.CharField(null=False)
    checksum = ChecksumField(null=False)
