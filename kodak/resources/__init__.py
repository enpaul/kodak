from typing import Tuple
from typing import Type

from kodak.resources._shared import KodakResource
from kodak.resources.alias import ImageAlias
from kodak.resources.heartbeat import Heartbeat
from kodak.resources.image import Image
from kodak.resources.openapi import OpenAPI


RESOURCES: Tuple[Type[KodakResource], ...] = (
    Heartbeat,
    Image,
    ImageAlias,
    OpenAPI,
)
