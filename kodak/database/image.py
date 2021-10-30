import peewee

from kodak import constants
from kodak.database._shared import ChecksumField
from kodak.database._shared import EnumField
from kodak.database._shared import KodakModel


class ImageRecord(KodakModel):
    """Model for source images"""

    name = peewee.Charfield(null=False)
    format = EnumField(constants.ImageFormat, null=False)
    deleted = peewee.BooleanField(null=False, default=False)
    checksum = ChecksumField(null=False)
