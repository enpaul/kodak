import json
import uuid
from typing import List

import peewee

from dehance.database._shared import DehanceModel


class ImageRecord(DehanceModel):
    """Database record for"""

    width = peewee.IntegerField(null=False)
    height = peewee.IntegerField(null=False)
    format = peewee.CharField(null=False)
    deleted = peewee.BooleanField(null=False, default=False)
    public = peewee.BooleanField(null=False, default=False)
    owner = peewee.UUIDField(null=False)
    sha256 = peewee.CharField(null=False)
    _readable = peewee.CharField(null=False, default="[]")

    @property
    def readable(self) -> List[uuid.UUID]:
        """List of UUIDs corresponding to accounts that can read the file"""
        return [uuid.UUID(item) for item in json.loads(self._readable)]

    @readable.setter
    def readable(self, value: List[uuid.UUID]):
        """Update the list of UUIDs for accounts that can read the file"""
        self._readable = json.dumps([str(item) for item in value])
