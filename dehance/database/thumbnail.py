import peewee

from dehance.database._shared import DehanceModel
from dehance.database.image import ImageRecord


class ThumbnailRecord(DehanceModel):

    parent = peewee.ForeignKeyField(ImageRecord)
    width = peewee.IntegerField(null=False)
    height = peewee.IntegerField(null=False)
