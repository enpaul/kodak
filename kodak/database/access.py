import peewee

from kodak.database._shared import KodakModel


class AccessRecord(KodakModel):
    """Model for access keys when operating in private mode"""

    password = peewee.CharField(null=False)
