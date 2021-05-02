import datetime
import uuid

import peewee


INTERFACE = peewee.DatabaseProxy()


class DehanceModel(peewee.Model):
    class Meta:  # pylint: disable=too-few-public-methods,missing-class-docstring
        database = INTERFACE

    uuid = peewee.UUIDField(null=False, unique=True, default=uuid.uuid4)
    created = peewee.DateTimeField(null=False, default=datetime.datetime.utcnow)
