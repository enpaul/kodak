import peewee

from fresnel_lens.database._shared import FresnelModel
from fresnel_lens.database.image import ImageRecord


class ThumbnailRecord(FresnelModel):

    parent = peewee.ForeignKeyField(ImageRecord)
    width = peewee.IntegerField(null=False)
    height = peewee.IntegerField(null=False)
