import datetime
import enum
import typing
import uuid
from typing import NamedTuple
from typing import Type

import peewee

if typing.TYPE_CHECKING:
    import _hashlib


INTERFACE = peewee.DatabaseProxy()


class Checksum(NamedTuple):
    """Checksum data container

    :param algorithm: Hashing algorithm, must be supported by Python's hashlib
    :param digest: Hex digest of the hash
    """

    algorithm: str
    digest: str

    @classmethod
    def from_hash(cls, data: "_hashlib.HASH"):
        """Construct from a hashlib object"""
        return cls(algorithm=data.name, digest=data.hexdigest())


class EnumField(peewee.CharField):
    """Custom field for storing enums"""

    def __init__(self, enumeration: Type[enum.Enum], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enumeration = enumeration

    def db_value(self, value: enum.Enum) -> str:
        """Convert the enum value to the database string

        :param value: Enum item to store the name of
        :raises peewee.IntegrityError: When the item passed to ``value`` is not in the field's enum
        :returns: The name of the enum item passed to ``value``
        """
        if not isinstance(value, self.enumeration):
            raise peewee.IntegrityError(
                f"Enum {self.enumeration.__name__} has no value '{value}'"
            )
        return value.name

    def python_value(self, value: str) -> enum.Enum:
        """Convert the stored string to the corresponding enum

        :param value: Name of the item from the field's enum to return
        :raises peewee.IntegrityError: When the name passed to ``value`` does not correspond to an
                                       item in the field's enum
        :returns: The enum item with the name passed to ``value``
        """
        try:
            return self.enumeration[value]
        except KeyError:
            raise peewee.InterfaceError(
                f"Enum {self.enumeration.__name__} has no value with name '{value}'"
            ) from None


class ChecksumField(peewee.CharField):
    """Field for storing checksum hashes in the database

    .. note:: The reason for implementing this is to protect against future changes to the hashing
              algorithm. Just storing the digest means that if the hashing algorithm is ever
              changed (for performance, etc) then any existing records will be invalidated. By
              storing the hashing algorithm with the digest we can protect against that possibility.
              A custom container needs to be implemented because the builtin hashlib has no way to
              recreate a hash object from the algorithm+digest without the original data.
    """

    def db_value(self, value: Checksum) -> str:
        """Serialize the checkstum to a database string"""
        return f"{value.algorithm}:{value.digest}"

    def python_value(self, value: str) -> Checksum:
        """Deserailize a string to a checksum container"""
        alg, _, digest = value.partition(":")
        return Checksum(algorithm=alg, digest=digest)


class KodakModel(peewee.Model):
    """Base model for defining common fields and attaching database"""

    class Meta:  # pylint: disable=too-few-public-methods,missing-class-docstring
        database = INTERFACE

    uuid = peewee.UUIDField(null=False, unique=True, default=uuid.uuid4)
    created = peewee.DateTimeField(null=False, default=datetime.datetime.utcnow)
