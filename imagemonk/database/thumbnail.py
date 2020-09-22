import peewee

from imagemonk.database._shared import ImageMonkModel
from imagemonk.database.image import ImageRecord


class ThumbnailRecord(ImageMonkModel):

    parent = peewee.ForeignKeyField(ImageRecord)
    width = peewee.IntegerField(null=False)
    height = peewee.IntegerField(null=False)
