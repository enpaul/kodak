import peewee

from kodak.database._shared import KodakModel
from kodak.database.image import ImageRecord


class ThumbnailRecord(KodakModel):

    parent = peewee.ForeignKeyField(ImageRecord)
    width = peewee.IntegerField(null=False)
    height = peewee.IntegerField(null=False)
