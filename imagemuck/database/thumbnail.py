import peewee

from imagemuck.database._shared import ImageMuckModel
from imagemuck.database.image import ImageRecord


class ThumbnailRecord(ImageMuckModel):

    parent = peewee.ForeignKeyField(ImageRecord)
    width = peewee.IntegerField(null=False)
    height = peewee.IntegerField(null=False)
