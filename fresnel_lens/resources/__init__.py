from typing import Tuple

from fresnel_lens.resources._shared import FresnelResource
from fresnel_lens.resources.alias import ImageAlias
from fresnel_lens.resources.heartbeat import Heartbeat
from fresnel_lens.resources.image import Image
from fresnel_lens.resources.openapi import OpenAPI


RESOURCES: Tuple[FresnelResource, ...] = (
    Heartbeat,
    Image,
    ImageAlias,
    OpenAPI,
)
